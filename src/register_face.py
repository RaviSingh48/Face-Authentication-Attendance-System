import cv2
import os
import time

name = input("Enter your name: ").strip()
if not name:
    raise ValueError("Name cannot be empty")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES_DIR = os.path.join(BASE_DIR, "data", "faces")
os.makedirs(FACES_DIR, exist_ok=True)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

if not cap.isOpened():
    raise RuntimeError("Camera not accessible")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

REGISTER_TIME = 2.0        # seconds face must stay
MISS_TOLERANCE = 0.5       # allowed miss duration

start_time = None
last_seen = None
saved = False

print("[INFO] Look straight at the camera for 2 seconds...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(80, 80)
    )

    now = time.time()

    if len(faces) > 0:
        (x, y, w, h) = max(faces, key=lambda b: b[2] * b[3])

        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        if start_time is None:
            start_time = now

        last_seen = now
        elapsed = now - start_time

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(
            frame,
            f"Hold still {elapsed:.1f}/2 sec",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0,255,0),
            2
        )

        if elapsed >= REGISTER_TIME:
            path = os.path.join(FACES_DIR, f"{name}.jpg")
            cv2.imwrite(path, face_img)
            print(f"[SUCCESS] Face registered: {path}")
            saved = True

    else:
        # face temporarily missing
        if last_seen and (now - last_seen) > MISS_TOLERANCE:
            start_time = None
            last_seen = None

        cv2.putText(
            frame,
            "Face not detected",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0,0,255),
            2
        )

    cv2.imshow("Register Face", frame)

    if saved or cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
cv2.destroyAllWindows()
