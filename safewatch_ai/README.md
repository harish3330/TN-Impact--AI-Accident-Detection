# SafeWatch AI - Industrial Accident Detection System

## Overview

SafeWatch AI is a real-time industrial safety monitoring system that uses computer vision to detect workplace accidents and safety violations. It processes video feeds from CCTV/webcam sources, identifies dangerous situations, and dispatches multi-channel alerts.

## Features

### Accident Detection
- **Fall Detection** - Person lying down (aspect ratio < 0.7) for ≥1.5 seconds
- **Motionless Body** - Person stationary for ≥4 seconds  
- **Zone Breach** - Person entering user-defined restricted areas
- **Unsafe Proximity** - Person too close to vehicles for ≥1.5 seconds
- **PPE Violations** - Placeholder for future safety equipment detection

### Alert System
- **Sound Alerts** - Configurable beeps (1 for warning, 3 for critical)
- **Email Alerts** - SMTP with annotated snapshot attachments
- **Incident Logging** - SQLite database with searchable history
- **Cooldown Period** - Prevents alert spam

## Quick Start

### Prerequisites
- Python 3.10+
- Webcam or video files for testing

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Configure email alerts (optional)
cp .env.example .env
# Edit .env with your SMTP credentials
```

### Running the Application

#### Web Dashboard (Recommended)
```bash
streamlit run dashboard/app.py
```
Access at: http://localhost:8501

#### CLI Mode
```bash
python main.py
```

## Project Structure

```
safewatch_ai/
├── README.md                   # This file
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── config/
│   └── camera_config.json      # Camera zones, thresholds, settings
├── dashboard/
│   ├── app.py                  # Streamlit web application
│   └── components/
│       ├── __init__.py
│       └── styles.py           # CSS and UI components
├── src/
│   ├── __init__.py
│   ├── detector.py             # YOLOv8 wrapper + tracking
│   ├── rule_engine.py          # Incident detection rules
│   ├── alert_system.py         # Email/sound/snapshot dispatcher
│   ├── video_capture.py        # Video source abstraction
│   └── utils/
│       ├── __init__.py
│       ├── geometry.py         # Math utilities
│       └── tracking.py         # Object tracking
├── data/
│   ├── incidents/              # Snapshots + SQLite DB
│   └── sample_videos/          # Demo footage
└── yolov8n.pt                  # YOLO model (auto-downloaded)
```

## Configuration

### Camera Setup
Edit `config/camera_config.json` to configure:
- Camera sources (webcam, RTSP, files)
- Restricted zones (polygons)
- Detection thresholds
- Alert settings

### Email Alerts
Create `.env` file:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
ALERT_EMAIL=your@gmail.com
ALERT_PASSWORD=app_password_here
DEFAULT_ALERT_EMAIL=safety@company.com
```

## Usage

### Web Dashboard
1. Navigate to **Live Monitor** page
2. Select video source (webcam or sample video)
3. Draw restricted zones if needed
4. Click **Start Monitoring**
5. Watch for real-time incident detection

### CLI Mode
1. Run `python main.py`
2. Select video source from menu
3. Press 'q' to quit

## Detection Types

| Type | Trigger | Severity | Sound |
|------|----------|----------|-------|
| FALL_DETECTED | Person horizontal (AR < 0.7) for 1.5s | CRITICAL | 3 beeps |
| MOTIONLESS_BODY | Person stationary for 4s | CRITICAL | 3 beeps |
| ZONE_BREACH | Person in restricted area | WARNING | 1 beep |
| UNSAFE_PROXIMITY | Person <100px from vehicle for 1.5s | WARNING | 1 beep |

## Tech Stack

- **Computer Vision**: YOLOv8 + OpenCV
- **Web Framework**: Streamlit
- **Database**: SQLite
- **Alerting**: Python smtplib + winsound
- **Dependencies**: See requirements.txt

## License

MIT License
