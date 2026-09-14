import uvicorn
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/login")
async def mock_login(credentials: LoginRequest):
    if credentials.email == "demo@student.edu" and credentials.password == "demo123":
        return {"access_token": "mock_demo_token_789", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

def generate_dynamic_timetable():
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    
    # Realistic varied schedule from 8:30 AM to 4:45 PM with lunch breaks
    weekly_schedule = {
        0: [ # Monday
            {"c": "Data Privacy and Security", "s": "08:30:00", "e": "10:30:00", "t": "Theory", "v": "Room 301", "f": "Dr. Alan"},
            {"c": "Generative AI", "s": "10:45:00", "e": "11:45:00", "t": "Theory", "v": "Room 205", "f": "Dr. Lovelace"},
            {"c": "Framework for Data and Visual Analytics", "s": "12:30:00", "e": "14:30:00", "t": "Lab", "v": "Data Lab 1", "f": "Dr. Smith"},
            {"c": "Problem Solving Techniques", "s": "14:45:00", "e": "16:45:00", "t": "Theory", "v": "Seminar Hall", "f": "Prof. Kumar"}
        ],
        1: [ # Tuesday
            {"c": "Generative AI", "s": "08:30:00", "e": "10:30:00", "t": "Lab", "v": "AI Lab 1", "f": "Dr. Lovelace"},
            {"c": "Data Privacy and Security", "s": "10:45:00", "e": "11:45:00", "t": "Theory", "v": "Room 301", "f": "Dr. Alan"},
            {"c": "Design Thinking and Innovation", "s": "12:30:00", "e": "15:30:00", "t": "Lab", "v": "Innovation Lab", "f": "Prof. Kumar"}
        ],
        2: [ # Wednesday
            {"c": "Framework for Data and Visual Analytics", "s": "09:00:00", "e": "10:00:00", "t": "Theory", "v": "Room 301", "f": "Dr. Smith"},
            {"c": "Data Privacy and Security", "s": "10:15:00", "e": "12:15:00", "t": "Lab", "v": "Cyber Lab", "f": "Dr. Alan"},
            {"c": "Generative AI", "s": "13:30:00", "e": "14:30:00", "t": "Theory", "v": "Room 205", "f": "Dr. Lovelace"}
        ],
        3: [ # Thursday
            {"c": "Problem Solving Techniques", "s": "08:30:00", "e": "09:30:00", "t": "Theory", "v": "Room 304", "f": "Prof. Kumar"},
            {"c": "Framework for Data and Visual Analytics", "s": "09:30:00", "e": "11:30:00", "t": "Theory", "v": "Room 301", "f": "Dr. Smith"},
            {"c": "Design Thinking and Innovation", "s": "12:30:00", "e": "13:30:00", "t": "Theory", "v": "Room 304", "f": "Prof. Kumar"},
            {"c": "Internship Tracking", "s": "13:45:00", "e": "15:45:00", "t": "Theory", "v": "Seminar Hall", "f": "Placement Cell"}
        ],
        4: [ # Friday
            {"c": "Data Privacy and Security", "s": "08:30:00", "e": "09:30:00", "t": "Theory", "v": "Room 301", "f": "Dr. Alan"},
            {"c": "Generative AI", "s": "09:30:00", "e": "10:30:00", "t": "Theory", "v": "Room 205", "f": "Dr. Lovelace"},
            {"c": "Framework for Data and Visual Analytics", "s": "10:45:00", "e": "12:45:00", "t": "Lab", "v": "Data Lab 1", "f": "Dr. Smith"}
        ]
    }
    
    timetable = []
    # Weekdays
    for i in range(5):
        day = start_of_week + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        for cls in weekly_schedule[i]:
            timetable.append({
                "courseName": cls["c"],
                "start": f"{date_str} {cls['s']}",
                "end": f"{date_str} {cls['e']}",
                "type": cls["t"],
                "venue": cls["v"],
                "faculty": cls["f"]
            })
    
    # Weekends (Holidays)
    for i in range(5, 7):
        day = start_of_week + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        timetable.extend([
            {"courseName": "Holiday / Weekend", "start": f"{date_str} 00:00:00", "end": f"{date_str} 23:59:59", "type": "Off", "venue": "N/A", "faculty": "N/A"}
        ])
        
    return timetable

def generate_course_history(comp_type="Theory"):
    now = datetime.now()
    history = []
    for i in range(1, 14):
        day = now - timedelta(days=i)
        if day.weekday() < 5:
            date_str = day.strftime("%Y-%m-%d")
            history.append({"start": f"{date_str} 09:00:00", "end": f"{date_str} 10:00:00", "status": "PRESENT", "comp": comp_type})
            if comp_type == "Lab" and i % 3 == 0:
                history.append({"start": f"{date_str} 10:30:00", "end": f"{date_str} 12:30:00", "status": "ABSENT", "comp": "Lab"})
    return history

@app.get("/api/dashboard")
async def get_dashboard_data(token: str):
    if token != "mock_demo_token_789":
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    return {
        "studentName": "Guest",
        "profileDetails": {
            "fullName": "Guest Demo",
            "programme": "B.Tech Artificial Intelligence & Data Science",
            "email": "demo@student.edu",
            "phone": "+91 0000000000",
            "batchYear": "2024",
            "quota": "General",
            "admissionType": "Regular"
        },
        "totalPresent": 185,
        "totalClasses": 215,
        "percentage": 86.04,
        "courses": [
            {
                "name": "Data Privacy and Security",
                "code": "AD23631",
                "credits": 4,
                "present": 42,
                "total": 45,
                "percentage": 93.3,
                "components": [
                    {"label": "Theory", "present": 42, "total": 45, "pct": 93.3, "status": "Safe", "safe": True}
                ],
                "history": generate_course_history("Theory"),
                "scheduled": [
                    {"courseName": "Data Privacy and Security", "start": f"{date_str} 08:30:00", "end": f"{date_str} 10:30:00", "type": "Theory", "venue": "Room 301"}
                ]
            },
            {
                "name": "Framework for Data and Visual Analytics",
                "code": "AD23632",
                "credits": 4,
                "present": 38,
                "total": 48,
                "percentage": 79.1,
                "components": [
                    {"label": "Theory", "present": 20, "total": 24, "pct": 83.3, "status": "Safe", "safe": True},
                    {"label": "Lab", "present": 18, "total": 24, "pct": 75.0, "status": "Safe", "safe": True}
                ],
                "history": generate_course_history("Lab"),
                "scheduled": [
                    {"courseName": "Framework for Data and Visual Analytics", "start": f"{date_str} 12:30:00", "end": f"{date_str} 14:30:00", "type": "Lab", "venue": "Data Lab 1"}
                ]
            },
            {
                "name": "Generative AI",
                "code": "AD23633",
                "credits": 3,
                "present": 28,
                "total": 39,
                "percentage": 71.7,
                "components": [
                    {"label": "Theory", "present": 28, "total": 39, "pct": 71.7, "status": "At Risk", "safe": False}
                ],
                "history": generate_course_history("Theory"),
                "scheduled": [
                    {"courseName": "Generative AI", "start": f"{date_str} 10:45:00", "end": f"{date_str} 11:45:00", "type": "Theory", "venue": "Room 205"}
                ]
            },
            {
                "name": "Design Thinking and Innovation",
                "code": "GE23627",
                "credits": 2,
                "present": 20,
                "total": 20,
                "percentage": 100.0,
                "components": [
                    {"label": "Lab", "present": 20, "total": 20, "pct": 100.0, "status": "Safe", "safe": True}
                ],
                "history": generate_course_history("Lab"),
                "scheduled": []
            }
        ],
        "timetable": generate_dynamic_timetable(),
        "semesters": [
            {
                "termName": "Semester 1",
                "sgpa": "9.20",
                "courses": [
                    {"name": "Mathematical Foundations for AI", "code": "MA23116", "credits": 4, "grade": "O", "gp": 10.0, "examId": "1", "termCourseId": "11"},
                    {"name": "Physics for Information Science", "code": "PH23132", "credits": 4, "grade": "O", "gp": 10.0, "examId": "1", "termCourseId": "12"},
                    {"name": "Programming using C", "code": "GE23131", "credits": 4, "grade": "A+", "gp": 9.0, "examId": "1", "termCourseId": "13"},
                    {"name": "Basic Electrical and Electronics", "code": "EE23133", "credits": 4, "grade": "A+", "gp": 9.0, "examId": "1", "termCourseId": "14"},
                    {"name": "Engineering Practices", "code": "GE23123", "credits": 2, "grade": "A", "gp": 8.0, "examId": "1", "termCourseId": "15"},
                    {"name": "Technical Communication I", "code": "HS23111", "credits": 2, "grade": "A+", "gp": 9.0, "examId": "1", "termCourseId": "16"},
                    {"name": "Heritage of Tamils", "code": "GE23117", "credits": 1, "grade": "O", "gp": 10.0, "examId": "1", "termCourseId": "17"}
                ]
            },
            {
                "termName": "Semester 2",
                "sgpa": "8.85",
                "courses": [
                    {"name": "Probability and Inferential Statistics", "code": "MA23214", "credits": 4, "grade": "A+", "gp": 9.0, "examId": "2", "termCourseId": "21"},
                    {"name": "Data Structures", "code": "CS23231", "credits": 5, "grade": "O", "gp": 10.0, "examId": "2", "termCourseId": "22"},
                    {"name": "Digital Principles and Architecture", "code": "IT23231", "credits": 4, "grade": "A+", "gp": 9.0, "examId": "2", "termCourseId": "23"},
                    {"name": "Engineering Graphics", "code": "GE23111", "credits": 4, "grade": "B+", "gp": 7.0, "examId": "2", "termCourseId": "24"},
                    {"name": "Python Programming Lab", "code": "CS23221", "credits": 2, "grade": "O", "gp": 10.0, "examId": "2", "termCourseId": "25"},
                    {"name": "Tamils and Technology", "code": "GE23217", "credits": 1, "grade": "A+", "gp": 9.0, "examId": "2", "termCourseId": "26"},
                    {"name": "Technical Communication II", "code": "HS23221", "credits": 1, "grade": "A", "gp": 8.0, "examId": "2", "termCourseId": "27"}
                ]
            },
            {
                "termName": "Semester 3",
                "sgpa": "8.65",
                "courses": [
                    {"name": "Database Management Systems", "code": "CS23332", "credits": 5, "grade": "A+", "gp": 9.0, "examId": "3", "termCourseId": "31"},
                    {"name": "Discrete Mathematics for AI", "code": "MA23313", "credits": 4, "grade": "A", "gp": 8.0, "examId": "3", "termCourseId": "32"},
                    {"name": "Principles of Artificial Intelligence", "code": "AI23231", "credits": 4, "grade": "O", "gp": 10.0, "examId": "3", "termCourseId": "33"},
                    {"name": "Design and Analysis of Algorithms", "code": "CS23331", "credits": 4, "grade": "B+", "gp": 7.0, "examId": "3", "termCourseId": "34"},
                    {"name": "Object Oriented Programming", "code": "CS23333", "credits": 4, "grade": "A+", "gp": 9.0, "examId": "3", "termCourseId": "35"}
                ]
            },
            {
                "termName": "Semester 4",
                "sgpa": "9.10",
                "courses": [
                    {"name": "Operating Systems", "code": "CS23431", "credits": 5, "grade": "A+", "gp": 9.0, "examId": "4", "termCourseId": "41"},
                    {"name": "Software Construction", "code": "CS23432", "credits": 4, "grade": "A+", "gp": 9.0, "examId": "4", "termCourseId": "42"},
                    {"name": "Fundamentals of Machine Learning", "code": "AI23331", "credits": 4, "grade": "O", "gp": 10.0, "examId": "4", "termCourseId": "43"},
                    {"name": "Optimization Techniques for AI", "code": "MA23434", "credits": 4, "grade": "O", "gp": 10.0, "examId": "4", "termCourseId": "44"},
                    {"name": "Statistical Analysis and Computing", "code": "AD23431", "credits": 3, "grade": "A+", "gp": 9.0, "examId": "4", "termCourseId": "45"},
                    {"name": "Web Technology and Mobile App", "code": "AI23431", "credits": 3, "grade": "A", "gp": 8.0, "examId": "4", "termCourseId": "46"}
                ]
            },
            {
                "termName": "Semester 5",
                "sgpa": "8.85",
                "courses": [
                    {"name": "Computer Networks", "code": "CS23532", "credits": 5, "grade": "A+", "gp": 9.0, "examId": "5", "termCourseId": "51"},
                    {"name": "Big Data Architecture", "code": "AD23531", "credits": 4, "grade": "A", "gp": 8.0, "examId": "5", "termCourseId": "52"},
                    {"name": "Principles of Data Science", "code": "AD23532", "credits": 4, "grade": "O", "gp": 10.0, "examId": "5", "termCourseId": "53"},
                    {"name": "Deep Learning", "code": "AI23531", "credits": 4, "grade": "A+", "gp": 9.0, "examId": "5", "termCourseId": "54"},
                    {"name": "Customer Analytics", "code": "AD23A31", "credits": 3, "grade": "A", "gp": 8.0, "examId": "5", "termCourseId": "55"},
                    {"name": "Image Processing and Vision", "code": "AD23B31", "credits": 3, "grade": "A+", "gp": 9.0, "examId": "5", "termCourseId": "56"}
                ]
            },
            {
                "termName": "Semester 6",
                "sgpa": "--",
                "courses": [
                    {"name": "Data Privacy and Security", "code": "AD23631", "credits": 4, "grade": "--", "gp": "--", "examId": "6", "termCourseId": "61"},
                    {"name": "Framework for Data and Visual Analytics", "code": "AD23632", "credits": 4, "grade": "--", "gp": "--", "examId": "6", "termCourseId": "62"},
                    {"name": "Generative AI", "code": "AD23633", "credits": 3, "grade": "--", "gp": "--", "examId": "6", "termCourseId": "63"},
                    {"name": "Design Thinking and Innovation", "code": "GE23627", "credits": 2, "grade": "--", "gp": "--", "examId": "6", "termCourseId": "64"},
                    {"name": "Problem Solving Techniques", "code": "GE23621", "credits": 1, "grade": "--", "gp": "--", "examId": "6", "termCourseId": "65"},
                    {"name": "Internship", "code": "AD23621", "credits": 3, "grade": "--", "gp": "--", "examId": "6", "termCourseId": "66"}
                ]
            }
        ]
    }

@app.post("/api/result_breakdown")
def get_result_breakdown():
    return {
        "components": [
            {
                "componentName": "Internal Assessment",
                "totalMarks": 40,
                "effectiveMarks": 36.5,
                "assessments": [
                    {"assessmentName": "CAT 1", "obtainedMarks": 45, "totalMarks": 50},
                    {"assessmentName": "CAT 2", "obtainedMarks": 42, "totalMarks": 50}
                ]
            },
            {
                "componentName": "Semester End Examination",
                "totalMarks": 60,
                "effectiveMarks": 52.0,
                "assessments": [
                    {"assessmentName": "Theory Exam", "obtainedMarks": 88, "totalMarks": 100}
                ]
            }
        ]
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)