 Face Authentication Attendance System

# Overview
This project implements a real-time Face Authentication Attendance System using Python and OpenCV.  
The system registers a user’s face via a webcam, authenticates the face in real time, and marks attendance with Punch-In and Punch-Out while preventing basic spoofing attempts.

---

# Features
- Real-time face registration using webcam
- Face authentication for registered users only
- Automated Punch-In and Punch-Out
- Attendance logging with timestamps (CSV)
- Basic spoof prevention using head-movement (left-right) verification
- Simple, clean, and modular project structure

---

# Technology Stack
- Python 3.10
- OpenCV
- NumPy
- CSV (for attendance storage)



  # Project Structure

- Face Authentication Attendance System/
│
├── data/
│ ├── faces/
│ │ ├── Ravi.jpg
│ │ └── Shivam.jpg
│ └── attendance.csv
│
├── src/
│ ├── register_face.py
│ ├── recognize_face.py
│ ├── liveness.py
│ └── utils.py
│
├── requirements.txt
└── README.md






# How It Works

# 1. Face Registration
- Webcam opens automatically
- User keeps face visible for 2 seconds
- Face image is automatically captured and stored
- No manual key input required

# 2. Face Recognition
- Live camera feed detects faces
- Detected face is matched against registered faces
- Only registered users are authenticated

# 3. Attendance Marking
- Punch-In is marked only once per session
- Punch-Out is marked only once after a minimum time gap
- Attendance is saved with timestamp in `attendance.csv`

# 4. Spoof Prevention
- User must turn head left and then right
- Prevents spoofing using static photos or videos
- Lightweight and assignment-appropriate liveness check

