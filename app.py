from email_alert import send_email

import cv2
import config

from detector import detect_people
from utils import play_alarm, save_intrusion

# Open webcam
cap = cv2.VideoCapture(config.CAMERA_INDEX)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

intrusion_active = False

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = detect_people(frame)

    annotated_frame = results[0].plot()

    # Draw Restricted Zone
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

    # People Count
    person_count = len(results[0].boxes)

    cv2.putText(
        annotated_frame,
        f"People Count: {person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
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

        cv2.putText(
            annotated_frame,
            "INTRUDER DETECTED!",
            (80, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
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

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
