import base64
import json
import requests
import re
import sqlite3
import os
import uvicorn
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, as_completed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

a = os.environ.get("DB_PATH", ".campus_portal.db")

def init_db():
    b = sqlite3.connect(a)
    b.execute("PRAGMA journal_mode=WAL")
    b.execute("PRAGMA synchronous=NORMAL")
    c = b.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_data (user_id TEXT PRIMARY KEY, plan_json TEXT, od_json TEXT)")
    b.commit()
    b.close()

init_db()

class AuthRequest(BaseModel):
    token: str
    user_id: str = ""
    user_name: str = ""

class BreakdownRequest(BaseModel):
    token: str
    user_id: str
    exam_id: str
    term_course_id: str

class SaveRequest(BaseModel):
    token: str
    user_id: str = ""
    plan_json: str
    od_json: str

def calc_margin(a, b):
    if b <= 0:
        return {"pct": 0.0, "status": "No classes", "safe": True, "margin": 0}
    c = round((a / b) * 100, 1)
    if c >= 75.0:
        d = int((a - 0.75 * b) // 0.75)
        e = "es"
        if d == 1:
            e = ""
        return {"pct": c, "status": f"Can bunk {max(0, d)} class{e}", "safe": True, "margin": max(0, d)}
    f = int(((0.75 * b) - a) // 0.25) + 1
    g = "es"
    if f == 1:
        g = ""
    return {"pct": c, "status": f"Need {f} class{g} for 75%", "safe": False, "margin": 0}

def get_user_id(a, b, c, d):
    e = None
    try:
        f = a.split(".")
        if len(f) >= 2:
            g = f[1] + "=" * ((4 - len(f[1]) % 4) % 4)
            h = json.loads(base64.urlsafe_b64decode(g))
            e = str(h.get("userId") or h.get("sub") or h.get("id") or h.get("ukid") or "")
    except Exception:
        pass
    if not e:
        try:
            i = requests.get(f"{d}/rest/personalDetails", headers=b, cookies=c, timeout=5)
            if i.status_code == 200:
                e = str(i.json().get("id") or "")
        except Exception:
            pass
    if e:
        j = re.search(r'\d+', e)
        if j:
            return j.group(0)
    return ""

def parse_sem_name(a, b):
    if not a:
        return f"Semester {b}"
    c = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8}
    d = re.search(r'\bSEM\s+([IVXLCDM]+)\b', a.upper())
    if d and d.group(1) in c:
        return f"Semester {c[d.group(1)]}"
    e = re.search(r'\bSEM(?:ESTER)?\s*(\d+)\b', a.upper())
    if e:
        return f"Semester {e.group(1)}"
    return f"Semester {b}"

@app.post("/api/attendance")
def fetch_data(a: AuthRequest):
    b = a.token.strip().strip('"').strip("'")
    if b.lower().startswith("bearer "):
        b = b[7:].strip()
    if not b:
        raise HTTPException(status_code=400, detail="Token required")
    
    c = "https://rajalakshmi.digiicampus.com"
    d = {"auth-token": b, "Authorization": f"Bearer {b}", "User-Agent": "Mozilla/5.0", "Accept": "application/json", "Origin": c, "Referer": f"{c}/"}
    e = {"user": b}
    
    f = a.user_id
    if not f:
        f = get_user_id(b, d, e, c)
    g = a.user_name
    if not g:
        g = "Student"
    h = "46"
    
    if not f:
        raise HTTPException(status_code=400, detail="Failed to resolve User ID")

    i = {}
    try:
        j = requests.get(f"{c}/rest/users/{f}/profile/personalDetails", headers=d, cookies=e, timeout=5)
        if j.status_code == 200:
            i = j.json()
            g = i.get("fullName") or g
    except Exception:
        pass

    try:
        k = requests.get(f"{c}/rest/programmeBatchTerms?batch=active", headers=d, cookies=e, timeout=5)
        if k.status_code == 200:
            l = k.json()
            m = []
            if isinstance(l, list):
                m = l
            else:
                m = l.get("terms", [])
            if m and isinstance(m[0], dict) and "id" in m[0]:
                h = str(m[0]["id"])
    except Exception:
        pass

    n = {}
    try:
        o = requests.get(f"{c}/api/attendance/student/{f}/term/{h}", headers=d, cookies=e, timeout=10)
        if o.status_code == 200:
            n = o.json()
        elif o.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=500, detail="Network error")

    p = []
    q = {}
    try:
        r = requests.get(f"{c}/rest/classes/v2/", headers=d, cookies=e, timeout=10)
        if r.status_code == 200:
            s = r.json()
            t = []
            if isinstance(s, list):
                t = s
            else:
                t = s.get("classes") or []
            for u in t:
                v = str(u.get("classId") or "")
                w = (u.get("name") or u.get("subjectName") or u.get("courseName") or "").replace('\xa0', ' ').strip()
                if v:
                    p.append(v)
                    q[v] = w
    except Exception:
        pass

    x = []
    if p:
        try:
            y = []
            for z in p:
                y.append(("classIds", z))
            aa = datetime.now()
            y.append(("from", (aa - timedelta(days=45)).strftime("%Y-%m-%d 05:30:00")))
            y.append(("to", (aa + timedelta(days=120)).strftime("%Y-%m-%d 05:30:00")))
            ab = requests.get(f"{c}/rest/classes/v2/lessons", headers=d, cookies=e, params=y, timeout=15)
            if ab.status_code == 200:
                ac = ab.json()
                if isinstance(ac, list):
                    x = ac
                else:
                    x = ac.get("lessons", [])
                    x.extend(ac.get("futureLessons", []))
        except Exception:
            pass

    ad = []
    ae = {}
    for af in x:
        if not isinstance(af, dict):
            continue
        ag = "Subject"
        ah = af.get("classList") or []
        if len(ah) > 0 and isinstance(ah[0], dict) and ah[0].get("courseName"):
            ag = ah[0].get("courseName")
        else:
            ai = af.get("classIds") or []
            if len(ai) > 0:
                ag = q.get(str(ai[0]), "Subject")
        ag = ag.replace('\xa0', ' ').strip()
        aj = ag.lower()
        
        ak = af.get("start") or af.get("startTime")
        al = af.get("end") or af.get("endTime")
        if not ak or not al:
            continue
        
        am = ""
        an = None
        if len(ah) > 0 and isinstance(ah[0], dict):
            am = (ah[0].get("batch") or "").lower()
            an = ah[0].get("courseComponentTypeId")
        ao = "Theory"
        if an == 2 or "practical" in am or "lab" in am:
            ao = "Lab"
        
        ap = "Classroom"
        aq = af.get("venueDetails")
        if isinstance(aq, dict) and aq.get("name"):
            ap = aq.get("name")
        else:
            ap = af.get("venue") or af.get("room") or "Classroom"
        
        ar = ""
        ast = af.get("facultyList") or []
        if len(ast) > 0 and isinstance(ast[0], dict) and ast[0].get("facultyName"):
            ar = ast[0].get("facultyName").replace('\xa0', ' ').strip()
        
        au = {"courseName": ag, "start": ak, "end": al, "type": ao, "venue": ap, "faculty": ar}
        ad.append(au)
        if aj not in ae:
            ae[aj] = []
        ae[aj].append(au)

    av = []
    aw = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for ax in n.get("courseAttendance", []):
        ay = (ax.get("courseName") or ax.get("subjectName") or ax.get("name") or "Subject").replace('\xa0', ' ').strip()
        az = ay.lower()
        ba = ax.get("totalPresent", 0)
        bb = ax.get("totalClasses", 0)
        bc = calc_margin(ba, bb)
        
        bd = []
        be = []
        
        for bf in ax.get("components", []):
            bg = bf.get("className") or bf.get("courseName") or ""
            bh = bf.get("courseComponentTypeId")
            bi = "Theory"
            if bh == 2 or "practical" in bg.lower() or "lab" in bg.lower():
                bi = "Lab"
            bj = bf.get("totalPresent", 0)
            bk = bf.get("totalClasses", 0)
            bl = calc_margin(bj, bk)
            bd.append({"label": bi, "name": bg, "present": bj, "total": bk, "pct": bl["pct"], "status": bl["status"], "safe": bl["safe"]})
            
            for bm in bf.get("attendance", []):
                bn = str(bm.get("lessonStartTime") or bm.get("date") or "")
                if not bn:
                    continue
                bo = bn.split(".")[0]
                if bo > aw:
                    continue

                raw_status = bm.get("finalStatus") or bm.get("status")
                is_marked = bm.get("isMarked")
                if is_marked is None:
                    is_marked = bm.get("marked")

                if is_marked is False or raw_status in ["NOT_MARKED", "UNMARKED", "PENDING", None]:
                    if raw_status in ["PRESENT", "ABSENT", "OD"]:
                        bp = raw_status
                    elif bm.get("present") is True:
                        bp = "PRESENT"
                    elif is_marked is False or raw_status is None:
                        bp = "NOT_MARKED"
                    else:
                        bp = "ABSENT"
                else:
                    bp = raw_status

                be.append({"comp": bi, "status": bp, "start": bo, "end": str(bm.get("lessonEndTime") or "").split(".")[0]})
                
        be.sort(key=lambda x: x.get("start") or "", reverse=True)
        bq = ae.get(az, [])
        bq.sort(key=lambda x: x.get("start") or "")
        
        av.append({"name": ay, "present": ba, "total": bb, "pct": bc["pct"], "status": bc["status"], "safe": bc["safe"], "margin": bc["margin"], "components": bd, "history": be, "scheduled": bq})
        
    ad.sort(key=lambda x: x.get("start") or "")
    
    br = 0
    if n.get("percentage"):
        br = round(n.get("percentage"), 2)
    return {
        "studentName": g, 
        "profileDetails": i,
        "totalPresent": n.get("totalPresent", 0), 
        "totalClasses": n.get("totalClasses", 0), 
        "percentage": br, 
        "courses": av, 
        "timetable": ad
    }

@app.post("/api/results")
def fetch_results(a: AuthRequest):
    b = a.token.strip().strip('"').strip("'")
    if b.lower().startswith("bearer "):
        b = b[7:].strip()
    
    c = "https://rajalakshmi.digiicampus.com"
    d = {"auth-token": b, "Authorization": f"Bearer {b}", "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    e = {"user": b}
    
    f = a.user_id
    if not f:
        f = get_user_id(b, d, e, c)
    if not f:
        return {"semesters": []}

    g = set()
    try:
        h = requests.get(f"{c}/rest/programmeBatchTerms", headers=d, cookies=e, timeout=4)
        if h.status_code == 200:
            i = h.json()
            j = []
            if isinstance(i, list):
                j = i
            else:
                j = i.get("terms", [])
            for k in j:
                if isinstance(k, dict) and k.get("id"):
                    g.add(int(k["id"]))
    except Exception:
        pass

    l = set()
    for m in range(1, 65):
        l.add(m)
    n = list(g.union(l))

    def o(p):
        q = f"{c}/api/v2/resultDeclaration/student/term/{p}/{f}"
        try:
            r = requests.get(q, headers=d, cookies=e, timeout=4)
            if r.status_code == 200 and len(r.text) > 20:
                s = r.json()
                if not isinstance(s, dict) or not s.get("courses"):
                    return None
                
                t = s.get("examId", "")
                
                u = []
                for v in s.get("courses", []):
                    w = str(v.get("grade") or v.get("finalGrade") or "--")
                    x = float(v.get("gradePoint") or v.get("finalGradePoint") or 0)
                    y = str(v.get("termCourseId", ""))
                    
                    if w.upper() == "U":
                        x = 0.0

                    u.append({
                        "name": v.get("courseName") or v.get("name") or "Subject",
                        "code": v.get("courseCode") or v.get("code") or "",
                        "credits": v.get("courseCredits") or v.get("creditHours") or v.get("credits") or 0,
                        "grade": w,
                        "gp": x,
                        "examId": t,
                        "termCourseId": y
                    })
                
                z = str(s.get("sgpa")) if s.get("sgpa") is not None else "--"
                return {
                    "tid": p,
                    "examName": s.get("examName") or "",
                    "sgpa": z,
                    "courses": u
                }
        except Exception:
            return None

    aa = []
    with ThreadPoolExecutor(max_workers=15) as ab:
        ac = []
        for ad in n:
            ac.append(ab.submit(o, ad))
        for ae in as_completed(ac):
            af = ae.result()
            if af:
                aa.append(af)

    aa.sort(key=lambda x: x["tid"])

    ag = []
    ah = set()
    for ai, aj in enumerate(aa):
        ak = parse_sem_name(aj["examName"], ai + 1)
        if ak in ah:
            ak = f"{ak} ({aj['tid']})"
        ah.add(ak)
        
        ag.append({
            "termName": ak,
            "sgpa": aj["sgpa"],
            "courses": aj["courses"]
        })
            
    return {"semesters": ag}

@app.post("/api/result_breakdown")
def get_result_breakdown(a: BreakdownRequest):
    b = a.token.strip().strip('"').strip("'")
    if b.lower().startswith("bearer "):
        b = b[7:].strip()
    c = "https://rajalakshmi.digiicampus.com"
    d = {"auth-token": b, "Authorization": f"Bearer {b}", "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    e = {"user": b}
    
    if not a.user_id or not a.exam_id or not a.term_course_id:
        return {}
        
    f = f"{c}/api/v2/resultDeclaration/student/course-breakdown/{a.exam_id}/{a.user_id}/{a.term_course_id}"
    try:
        g = requests.get(f, headers=d, cookies=e, timeout=5)
        if g.status_code == 200:
            return g.json()
    except Exception:
        pass
    return {}

@app.post("/api/user_data/save")
def save_user_data(a: SaveRequest):
    if not a.user_id:
        return {"status": "error", "detail": "Missing"}
    b = sqlite3.connect(os.environ.get("DB_PATH", ".campus_portal.db"))
    c = b.cursor()
    c.execute("INSERT OR REPLACE INTO user_data (user_id, plan_json, od_json) VALUES (?, ?, ?)", (a.user_id, a.plan_json, a.od_json))
    b.commit()
    b.close()
    return {"status": "success"}

@app.post("/api/user_data/load")
def load_user_data(a: AuthRequest):
    if not a.user_id:
        return {"plan": {}, "ods": {}}
    b = sqlite3.connect(os.environ.get("DB_PATH", ".campus_portal.db"))
    c = b.cursor()
    c.execute("SELECT plan_json, od_json FROM user_data WHERE user_id=?", (a.user_id,))
    d = c.fetchone()
    b.close()
    if d:
        return {"plan": json.loads(d[0]), "ods": json.loads(d[1])}
    return {"plan": {}, "ods": {}}

if __name__ == "__main__":
    a = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=a)