# Face Recognition Attendance System

A real-time Face Recognition Attendance System built using Python, Streamlit, PostgreSQL, DeepFace, OpenCV, and WebRTC.

This project allows:

* Register students/employees using face recognition
* Store face embeddings in PostgreSQL
* Detect and recognize faces in real time
* Automatically mark IN/OUT attendance
* Admin dashboard with login
* Manage users (update/delete)
* View attendance history
* Track unknown faces
* Live gate camera attendance
* Audio notification on successful attendance

---

# Project Demo

Features implemented:

* Face registration
* Duplicate face prevention
* Live face recognition
* Attendance logging
* IN / OUT tracking
* Unknown face tracking
* Student attendance analytics
* Admin dashboard
* Live camera attendance

---

# Folder Structure

```text
face_recog/
│
├── dashboard.py
├── recognize.py
├── live_attendance.py
├── attendance.py
├── admin_registration.py
├── database_setup.py
├── register.py
├── generate_embeddings.py
├── requirements.txt
│
├── dataset/
│   └── student_images
│
├── sounds/
│   └── success.wav
│
├── unknown_faces/
│
├── haarcascade_frontalface_default.xml
│
└── README.md
```

---

# Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Backend                   |
| Streamlit  | Dashboard                 |
| PostgreSQL | Database                  |
| OpenCV     | Camera and face detection |
| DeepFace   | Face embeddings           |
| WebRTC     | Live stream               |
| SQLAlchemy | Database integration      |
| Plotly     | Analytics                 |

---

# Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/face-recognition-attendance.git

cd face-recognition-attendance
```

Replace:

```text
YOUR_USERNAME
```

with your GitHub username.

---

# Step 2: Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Expected:

```text
(venv)
```

---

# Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

---

# Step 4: Install PostgreSQL

Download PostgreSQL:

[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

Install pgAdmin during setup.

Remember your:

* Username
* Password
* Port

Example:

```text
Username: postgres
Password: 1234
Port: 5432
```

---

# Step 5: Create Database

Open pgAdmin:

```text
Servers
    PostgreSQL
        Databases
```

Create:

```text
face_recognition_db
```

---

# Step 6: Update Database Credentials

Open:

```python
attendance.py
```

Update:

```python
host="localhost"
port="5432"
database="face_recognition_db"
user="postgres"
password="your_password"
```

Do the same in:

* dashboard.py
* admin_registration.py
* database_setup.py
* recognize.py

---

# Step 7: Create Tables Automatically

Run:

```bash
python database_setup.py
```

Expected:

```text
Database setup complete
```

Tables created:

* people_master
* attendance_logs
* admin_users
* unknown_faces

Default Admin:

```text
Username: admin
Password: admin123
```

---

# Step 8: Download Haar Cascade

Download:

[https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)

Place file in project root.

---

# Step 9: Add Notification Sound

Create:

```text
sounds/
```

Place:

```text
success.wav
```

inside.

---

# Step 10: Start Dashboard

Run:

```bash
streamlit run dashboard.py
```

Expected:

```text
Local URL:
http://localhost:8501
```

Open browser.

---

# How Registration Works

1. Login as Admin
2. Open Register User
3. Enter details
4. Open camera
5. Capture face embeddings
6. Click Complete Registration

System automatically:

* checks duplicate faces
* creates embedding
* stores in PostgreSQL

---

# How Attendance Works

1. Open Live Attendance
2. Camera starts
3. Face detected
4. Student recognized
5. Attendance automatically marked

Attendance flow:

```text
First scan → IN
Second scan → OUT
Third scan → IN
```

Duplicate scans within one minute are ignored.

---

# Manage Users

Admin can:

* Edit student information
* Delete users
* Remove datasets

---

# Unknown Face Tracking

If face not recognized:

```text
Unknown
```

System stores image and logs it.

---

# Future Improvements

Planned:

* Attendance percentage
* Monthly calendar view
* PDF reports
* Excel export
* Email notifications
* Mask detection
* Mobile support
* Docker deployment
* Cloud database support

---

# Troubleshooting

### Camera not opening

Close:

* Zoom
* Teams
* Browser tabs using camera

---

### PostgreSQL connection error

Check:

* PostgreSQL service running
* Password correct
* Port 5432

---

### Face not detected

Improve:

* Lighting
* Face position
* Camera quality

---

### Module not found

Run:

```bash
pip install -r requirements.txt
```

---

# Author

Built as a collage project for learning Computer Vision, Face Recognition, PostgreSQL and Streamlit.
