from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO("yolov8n.pt")

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

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

    # Check if any person is inside the restricted zone
    intruder_detected = False

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Calculate center point of the person
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Draw the center point
        cv2.circle(annotated_frame, (center_x, center_y), 5, (255, 0, 0), -1)

        # Check if center point is inside the restricted zone
        if (zone_x1 < center_x < zone_x2) and (zone_y1 < center_y < zone_y2):
            intruder_detected = True

    # Display alert if intruder detected
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

    # Show the frame
    cv2.imshow("Smart CCTV - Live Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
