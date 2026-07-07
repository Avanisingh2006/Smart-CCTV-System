from email_alert import send_email
import cv2
import config
import time
from datetime import datetime

from detector import detect_people
from utils import play_alarm, save_intrusion


# ==========================
# Select Video Source
# ==========================

def get_video_capture():

    print("\n========== SMART CCTV ==========")
    print("1. Live Webcam")
    print("2. Video File")
    print("3. IP Camera")
    print("===============================\n")

    choice = input("Select input source (1/2/3): ")

    if choice == "1":
        print("Using Webcam...")
        return cv2.VideoCapture(config.CAMERA_INDEX), "Webcam"

    elif choice == "2":
        print("Using Video File...")
        return cv2.VideoCapture(config.VIDEO_PATH), "Video File"

    elif choice == "3":
        print("Using IP Camera...")
        return cv2.VideoCapture(config.IP_CAMERA_URL), "IP Camera"

    else:
        print("Invalid choice. Using Webcam.")
        return cv2.VideoCapture(config.CAMERA_INDEX), "Webcam"


cap, source_name = get_video_capture()

if not cap.isOpened():
    print("Error: Could not open source.")
    exit()


intrusion_active = False

prev_time = time.time()


while True:

    ret, frame = cap.read()

    if not ret:

        if source_name == "Video File":
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        break

    results = detect_people(frame)

    annotated_frame = results[0].plot()

    # ==========================
    # FPS
    # ==========================

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    # ==========================
    # Header Background
    # ==========================

    cv2.rectangle(
        annotated_frame,
        (0, 0),
        (annotated_frame.shape[1], 110),
        (40, 40, 40),
        -1
    )

    # ==========================
    # Title
    # ==========================

    cv2.putText(
        annotated_frame,
        "AI SMART CCTV SURVEILLANCE",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )

    # ==========================
    # Camera ID
    # ==========================

    cv2.putText(
        annotated_frame,
        "CAM-01",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # ==========================
    # REC
    # ==========================

    cv2.circle(
        annotated_frame,
        (200, 65),
        8,
        (0, 0, 255),
        -1
    )

    cv2.putText(
        annotated_frame,
        "REC",
        (215, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ==========================
    # Timestamp
    # ==========================

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cv2.putText(
        annotated_frame,
        timestamp,
        (650, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ==========================
    # FPS
    # ==========================

    cv2.putText(
        annotated_frame,
        f"FPS : {int(fps)}",
        (650, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # ==========================
    # Source
    # ==========================

    cv2.putText(
        annotated_frame,
        f"Source : {source_name}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2
    )

    # ==========================
    # Status
    # ==========================

    cv2.putText(
        annotated_frame,
        "SYSTEM STATUS : ONLINE",
        (350, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # ==========================
    # Restricted Zone
    # ==========================

    cv2.rectangle(
        annotated_frame,
        (config.ZONE_X1, config.ZONE_Y1),
        (config.ZONE_X2, config.ZONE_Y2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        "Restricted Zone",
        (config.ZONE_X1, config.ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    person_count = len(results[0].boxes)

    cv2.putText(
        annotated_frame,
        f"People : {person_count}",
        (20, 145),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    intruder = False

    for box in results[0].boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        cv2.circle(
            annotated_frame,
            (cx, cy),
            5,
            (255, 0, 0),
            -1
        )

        if (
            config.ZONE_X1 < cx < config.ZONE_X2
            and
            config.ZONE_Y1 < cy < config.ZONE_Y2
        ):
            intruder = True

    if intruder:

        cv2.rectangle(
            annotated_frame,
            (180, 170),
            (720, 230),
            (0, 0, 255),
            -1
        )

        cv2.putText(
            annotated_frame,
            "INTRUDER DETECTED!",
            (220, 212),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

        if not intrusion_active:

            intrusion_active = True

            play_alarm(config.ALARM_SOUND)

            filename = save_intrusion(
                annotated_frame,
                config.CAPTURE_FOLDER,
                config.LOG_FILE
            )

            if filename:
                send_email(filename)

    else:

        intrusion_active = False

    cv2.imshow(
        "Smart CCTV Surveillance System",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

