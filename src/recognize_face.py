import cv2
import time
import os
import numpy as np
from utils import mark_attendance
from liveness import HeadTurnChecker

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES_DIR = os.path.join(BASE_DIR, "data", "faces")

# ================= FACE DETECTOR =================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================= LOAD REGISTERED FACES =================
faces = []
labels = []
names = {}
label_id = 0

for file in os.listdir(FACES_DIR):
    img_path = os.path.join(FACES_DIR, file)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        continue

    # 🔥 IMPORTANT PREPROCESSING
    img = cv2.resize(img, (200, 200))
    img = cv2.equalizeHist(img)

    faces.append(img)
    labels.append(label_id)
    names[label_id] = os.path.splitext(file)[0]
    label_id += 1

if len(faces) == 0:
    raise RuntimeError("No registered faces found")

# ================= TRAIN MODEL =================
model = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8
)
model.train(faces, np.array(labels))
print("[INFO] Model trained with", len(faces), "faces")

# ================= CAMERA =================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

attendance = {}
THRESHOLD = 70    # 🔥 tuned threshold
MIN_GAP = 10

head_turn = HeadTurnChecker()

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80)
    )

    frame_width = frame.shape[1]

    for (x, y, w, h) in detected_faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))
        face = cv2.equalizeHist(face)

        label, confidence = model.predict(face)

        if confidence < THRESHOLD:
            name = names[label]
        else:
            name = "Unknown"

        # ========== SPOOF PREVENTION ==========
        is_live = head_turn.update(x, frame_width)

        if name != "Unknown" and is_live:
            now = time.time()

            if name not in attendance:
                mark_attendance(name, "Punch-In")
                attendance[name] = {"in": True, "out": False, "time": now}
                print(f"[INFO] Punch-In: {name}")

            elif attendance[name]["in"] and not attendance[name]["out"]:
                if now - attendance[name]["time"] >= MIN_GAP:
                    mark_attendance(name, "Punch-Out")
                    attendance[name]["out"] = True
                    head_turn.reset()
                    print(f"[INFO] Punch-Out: {name}")

        # ========== DISPLAY ==========
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(
            frame,
            f"{name} ({int(confidence)})",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0) if name != "Unknown" else (0,0,255),
            2
        )

    cv2.putText(
        frame,
        "Turn head LEFT then RIGHT",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,255),
        2
    )

    cv2.imshow("Face Authentication Attendance System", frame)

    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
cv2.destroyAllWindows()
