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

    # Draw detections on the frame
    annotated_frame = results[0].plot()

    # Count people
    person_count = len(results[0].boxes)

    # Display the count on the frame
    cv2.putText(
        annotated_frame,
        f"People Count: {person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show the frame
    cv2.imshow("Smart CCTV - Live Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
