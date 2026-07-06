# Smart CCTV Surveillance System

An AI-powered real-time CCTV surveillance system that detects human intrusion using YOLOv8, captures evidence, and sends email alerts automatically.

---

## Features

- Real-time person detection using YOLOv8
- Detects intrusion in a restricted zone
- Automatically captures intruder images
- Sends email alerts with the captured image attached
- Plays an alarm sound when intrusion is detected
- Logs intrusion events for future reference

---

## Tech Stack

- Python
- OpenCV
- YOLOv8 (Ultralytics)
- SMTP (Email Notifications)
- python-dotenv
- Playsound

---

## Project Structure

```
smart-cctv-system/
│── app.py
│── detector.py
│── email_alert.py
│── config.py
│── utils.py
│── requirements.txt
│── README.md
│── .env.example
│── captures/
│── sounds/
```

---

## Installation

1. Clone the repository

```bash
git clone <repository-url>
cd smart-cctv-system
```

2. Install the required packages

```bash
pip install -r requirements.txt
```

---

## Email Alert Configuration

This project uses environment variables to securely store email credentials.

### Step 1: Create a `.env` file

Copy the `.env.example` file and rename it to `.env`.

### Step 2: Add your email credentials

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=receiver@example.com
```

> **Note:** If you're using Gmail, create an **App Password** and use it instead of your normal Gmail password.

---

## Running the Project

```bash
python app.py
```

---

## Future Improvements

- Face recognition for authorized personnel
- Multi-camera support
- Live web dashboard
- SMS and Telegram alerts
- Cloud storage for captured images

---

## Author

**Avani**
