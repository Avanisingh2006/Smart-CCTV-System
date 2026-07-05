from ultralytics import YOLO
import cv2
import os
from datetime import datetime

# Load the YOLO model
model = YOLO("yolov8n.pt")

# Create captures folder if it doesn't exist
os.makedirs("captures", exist_ok=True)

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# This prevents saving hundreds of screenshots
screenshot_taken = False

while True:
    # Read a frame
    ret, frame = cap.read()

    if not ret:
        break

    # Run YOLO detection (people only)
    results = model(
        frame,
        classes=[0],
        conf=0.5
    )

    # Draw detections
    annotated_frame = results[0].plot()

    # Restricted zone
    zone_x1, zone_y1 = 100, 100
    zone_x2, zone_y2 = 500, 400

    cv2.rectangle(
        annotated_frame,
        (zone_x1, zone_y1),
        (zone_x2, zone_y2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        "Restricted Zone",
        (zone_x1, zone_y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    # Count people
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

    intruder_detected = False

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        cv2.circle(annotated_frame, (center_x, center_y), 5, (255, 0, 0), -1)

        if (zone_x1 < center_x < zone_x2) and (zone_y1 < center_y < zone_y2):
            intruder_detected = True

    if intruder_detected:
        cv2.putText(
            annotated_frame,
            "INTRUDER DETECTED!",
            (100, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        # Save only one screenshot per intrusion
        if not screenshot_taken:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"captures/intruder_{timestamp}.jpg"

            cv2.imwrite(filename, annotated_frame)
            print(f"Screenshot saved: {filename}")

            screenshot_taken = True

    else:
        # Reset after intruder leaves
        screenshot_taken = False

    # Show the frame
    cv2.imshow("Smart CCTV - Live Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
