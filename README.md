# Smart CCTV Surveillance System

A real-time AI-powered CCTV surveillance system that detects human intrusion using YOLOv8, captures evidence, and sends email alerts automatically.

## Features

- Real-time person detection
- Intrusion image capture
- Automatic email alerts
- Alarm sound on detection
- Intrusion logging
- Modular Python code

## Tech Stack

- Python
- OpenCV
- YOLOv8 (Ultralytics)
- SMTP (Email)
- Playsound

## Project Structure

```
smart-cctv-system/
│── app.py
│── detector.py
│── email_alert.py
│── config.py
│── utils.py
│── test_sound.py
│── requirements.txt
│── README.md
│── captures/
│── sounds/
```

## Installation

```bash
git clone <repository-url>
cd smart-cctv-system
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Future Improvements

- Face Recognition
- Multi-camera support
- Web dashboard
- SMS notifications
- Cloud storage integration

## Author

Avani
