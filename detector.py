from ultralytics import YOLO
import config

# Load YOLO model only once
model = YOLO("yolov8n.pt")


def detect_people(frame):
    """
    Detect only people in the frame.
    Returns YOLO results.
    """
    results = model(
        frame,
        classes=[0],
        conf=config.CONFIDENCE,
        verbose=False
    )

    return results
    