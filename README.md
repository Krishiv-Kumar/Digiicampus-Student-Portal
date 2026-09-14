# Student Portal Architecture Demo 🎓

**Disclaimer:** This project is a standalone technical demonstration of a Progressive Web App (PWA) and decoupled backend architecture. It utilizes a fully mocked local dataset and does not integrate with, scrape, or connect to any live institutional systems.

**Student Portal Architecture Demo** is a high-performance, mobile-responsive, dark-themed web dashboard designed to showcase modern full-stack development practices. It features a streamlined UI/UX tailored for data visualization, predictive analytics, and academic management simulation based on a B.Tech Artificial Intelligence and Data Science curriculum.

## 🚀 Live Demo
**[View the Live Application Here]** *(Add your GitHub Pages URL here once generated)*

*Note for Recruiters: Use the provided mock credentials on the login screen to explore the fully functional dashboard using a simulated dataset.*

---

## ✨ Key Features

### 1. Stateful Attendance & Projection Engine
* **Data Visualization:** Processes and securely visualizes complex attendance datasets via REST API endpoints, rendering overall percentages and course-by-course breakdowns.
* **Dynamic Simulation:** Features a client-side predictive engine allowing users to toggle hypothetical "Bunk" or "Attend" statuses to calculate real-time impacts on projected attendance.
* **Leave Management Analytics:** Includes logic to input On-Duty (OD) leaves, dynamically recalculating margins to maintain required attendance thresholds.

### 2. Grade Simulation & CGPA Tracking
* **Mock Academic Records:** Renders historical SGPA and course data structures delivered from the FastAPI mock backend across all semesters in ascending order.
* **Predictive Grade Selector:** A built-in calculator utilizing custom JavaScript algorithms to forecast future SGPA and cumulative CGPA outcomes based on user-selected expected grades.

### 3. Interactive Vertical Timetable
* **Precision Grid:** Features a professional, 80px-per-hour vertical calendar schedule spanning a full seven-day week, correctly rendering both active classes and weekend/holiday states.
* **Time Tracking Logic:** A dynamic tracking line indicates the current time, actively highlighting ongoing classes and providing automated countdowns to the next session based on the device's local clock.

---

## 🛠 Tech Stack & Architecture

### Frontend (Progressive Web App)
* **HTML5 & Vanilla JavaScript:** Lightweight, zero-build-step architecture optimized for maximum rendering speed and DOM manipulation.
* **Tailwind CSS:** Utility-first styling utilized for a modern, responsive, and consistent dark-mode UI, incorporating mobile safe-area adaptations for native-app feel.
* **State Management:** Utilizes browser `localStorage` and PWA service workers for fast, persistent data retrieval and cross-session state handling.

### Backend (REST API)
* **Python FastAPI:** A high-performance, asynchronous REST framework serving the mock data layer and simulated authentication endpoints.
* **Pydantic:** Enforces strict type hinting and data validation for all API responses and login payloads.
* **CORS & Middleware:** Configured to cleanly handle cross-origin resource sharing between the static frontend host and the backend deployment environment.

---

## 📂 Project Structure

```text
├── .gitignore              # Hides Python cache and local environment files
├── index.html              # Main application entry point, login form, and UI
├── manifest.json           # PWA manifest for native app installation
├── README.md               # Project documentation
├── requirements.txt        # Python backend dependencies (FastAPI, Uvicorn, Pydantic)
├── main.py                 # FastAPI backend serving mock JSON endpoints and auth logic
└── sw.js                   # PWA service worker for asset caching