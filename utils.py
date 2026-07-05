import csv
import os
import threading
import winsound
from datetime import datetime


def play_alarm(sound_file):
    threading.Thread(
        target=lambda: winsound.PlaySound(
            sound_file,
            winsound.SND_FILENAME
        ),
        daemon=True
    ).start()


def save_intrusion(frame, capture_folder, log_file):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(
        capture_folder,
        f"intruder_{timestamp}.jpg"
    )

    os.makedirs(capture_folder, exist_ok=True)

    import cv2
    cv2.imwrite(filename, frame)

    file_exists = os.path.isfile(log_file)

    with open(log_file, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Time", "Screenshot"])

        writer.writerow([timestamp, filename])

    print(f"Intrusion saved: {filename}")

    return filename
    