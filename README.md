# Student Portal 🎓

**Student Portal** is a high-performance, mobile-responsive, dark-themed web dashboard designed as an advanced wrapper for the Rajalakshmi Engineering College Digiicampus portal. It replaces traditional academic interfaces with a streamlined UI/UX tailored for real-time tracking, predictive analytics, and enhanced academic management.

## 🚀 Live Demo
**[View the Live Application Here]** *(Add your GitHub Pages URL here once generated)*

*Note for Recruiters: Click the **"Try Demo"** button on the login screen to explore the fully functional dashboard using a simulated 6th-semester B.Tech dataset, bypassing the need for institutional credentials.*

---

## ✨ Key Features

### 1. Real-Time Attendance & Projection Engine
* **Live Tracking:** Securely fetches and visualizes the student's actual current attendance percentages, total classes conducted, and absentee records across all enrolled courses.
* **Dynamic Simulation:** Toggle hypothetical "Bunk" or "Attend" statuses for upcoming classes to view real-time changes to the projected attendance percentage.
* **Leave Management:** Input On-Duty (OD) leaves to instantly recalculate margins, helping students safely maintain mandatory attendance thresholds.

### 2. Grade Simulation & CGPA Tracking
* **Institutional Sync:** Pulls verified academic history and SGPA data directly from the university's database.
* **Predictive Grade Selector:** A built-in calculator that allows users to input expected grades for current courses to forecast future SGPA and cumulative CGPA outcomes.

### 3. Interactive Vertical Timetable
* **Precision Grid:** Features a professional, 80px-per-hour vertical calendar schedule starting at 7:30 AM.
* **Real-Time Tracking:** A dynamic tracking line indicates the current time, actively highlighting ongoing classes and providing countdowns to the next session.

---

## 🛠 Tech Stack & Architecture

### Frontend
* **HTML5 & Vanilla JavaScript:** Lightweight, zero-build-step architecture for maximum speed and easy deployment.
* **Tailwind CSS (CDN):** Utility-first styling utilized for a modern, responsive, and consistent dark-mode UI.
* **State Management:** Utilizes browser `localStorage` for fast, persistent data retrieval across sessions without unnecessary database queries.

### Backend
* **Python FastAPI:** A high-performance, asynchronous REST framework serving as a secure proxy between the client and the university's official servers.
* **Requests & Pydantic:** Handles secure API requests, payload validation, and data parsing.
* **SQLite:** Lightweight local database management for session handling and state persistence.
* **Authentication Architecture:** Implements a token-based security model that extracts active session cookies to bypass legacy CAPTCHA bottlenecks safely and efficiently.

---

## 📂 Project Structure

```text
├── .gitignore              # Hides local databases and Python cache
├── demo_data.js            # Fictional 6th-semester dataset for Recruiter Demo Mode
├── index.html              # Main application entry point and UI
├── requirements.txt        # Python backend dependencies
└── server.py               # FastAPI proxy server and routing
