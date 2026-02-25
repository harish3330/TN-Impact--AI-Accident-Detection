# SafeWatch AI — Industrial Accident Detection System

## Overview

SafeWatch AI is a real-time industrial safety monitoring system that uses
computer vision (YOLOv8) to detect workplace accidents and safety violations.
It processes video feeds from CCTV / webcam / RTSP sources, identifies dangerous
situations, and dispatches multi-channel alerts.

## Features

### Accident Detection
- **Fall Detection** — Person lying down (aspect ratio < 0.8) for ≥ 4 frames
- **Sudden Fall** — Rapid aspect-ratio drop from upright to horizontal
- **Motionless Body** — Person stationary for ≥ 8 frames
- **Zone Breach** — Person entering user-defined restricted polygon areas
- **Unsafe Proximity** — Person within 150 px of a vehicle for ≥ 3 frames
- **Person-Vehicle Impact** — Person bbox overlapping vehicle bbox (IoU > 0.05)
- **Vehicle Collision** — Two vehicle bboxes overlapping (IoU > 0.08 or centroids < 80 px)
- **PPE Violations** — Placeholder for future safety-equipment detection

### Alert System
- **Sound Alerts** — Configurable beeps (1 for warning, 3 for critical)
- **Email Alerts** — SMTP with annotated snapshot attachments
- **Incident Logging** — SQLite database with searchable history
- **Cooldown Period** — Prevents alert spam (configurable)

### Dashboard
- **Dual Theme** — Light / dark mode toggle in sidebar
- **Live Monitor** — Real-time video feed with detection overlay
- **Incident Log** — Searchable table with CSV export
- **Analytics** — Plotly charts: type breakdown, severity, timeline, hourly pattern
- **Configuration** — Camera, zone, alert, and detection parameter editors

## Quick Start

### Prerequisites
- Python 3.10+
- Webcam or video files for testing

### Installation
```bash
pip install -r requirements.txt

# Configure email alerts (optional)
cp .env.example .env
# Edit .env with your SMTP credentials
```

### Running

#### Web Dashboard (Recommended)
```bash
cd safewatch_ai
streamlit run dashboard/app.py
```
Access at http://localhost:8501

#### CLI Mode
```bash
cd safewatch_ai
python main.py
```

## Project Structure

```
safewatch_ai/
├── main.py                         # CLI entry point
├── requirements.txt                # Python dependencies
├── yolov8n.pt                      # YOLOv8 nano model
├── config/
│   └── camera_config.json          # Cameras, zones, thresholds, alerts
├── dashboard/
│   ├── app.py                      # Streamlit web dashboard
│   └── components/
│       ├── __init__.py
│       └── enhanced_bootstrap_styles.py  # CSS themes & UI renderers
├── src/
│   ├── __init__.py
│   ├── detector.py                 # YOLOv8 wrapper + simple tracker
│   ├── rule_engine.py              # Incident detection rules
│   ├── alert_system.py             # Email / sound / snapshot dispatcher
│   ├── video_capture.py            # Video source abstraction
│   └── utils/
│       ├── __init__.py
│       ├── geometry.py             # Bbox maths & polygon operations
│       └── tracking.py             # Per-object state tracker
├── data/
│   ├── incidents/                  # Snapshots + SQLite DB (auto-created)
│   └── sample_videos/              # Test footage
└── .env.example                    # SMTP config template
```

## Configuration

### Camera Setup
Edit `config/camera_config.json`:
- Camera sources (webcam index, RTSP URL, file path)
- Restricted zones (polygon point lists)
- Detection thresholds (fall AR, proximity px, frame counts)
- Alert contacts

### Email Alerts
Create a `.env` file from the template:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
ALERT_EMAIL=your@gmail.com
ALERT_PASSWORD=app_password_here
DEFAULT_ALERT_EMAIL=safety@company.com
```

## Detection Types

| Type | Trigger | Severity |
|------|---------|----------|
| FALL_DETECTED | Person horizontal (AR < 0.8) for 4+ frames | CRITICAL |
| SUDDEN_FALL | Rapid AR drop (standing → lying in one frame) | CRITICAL |
| MOTIONLESS_BODY | Person stationary for 8+ frames | CRITICAL |
| ZONE_BREACH | Person centroid inside restricted polygon | WARNING |
| UNSAFE_PROXIMITY | Person < 150 px from vehicle for 3+ frames | WARNING |
| PERSON_VEHICLE_IMPACT | Person-vehicle bbox IoU > 0.05 for 2+ frames | CRITICAL |
| VEHICLE_COLLISION | Vehicle-vehicle IoU > 0.08 for 2+ frames | CRITICAL |

## Tech Stack

- **Computer Vision**: YOLOv8 (ultralytics) + OpenCV
- **Web Framework**: Streamlit
- **Charts**: Plotly
- **Database**: SQLite
- **Alerting**: smtplib + winsound
- **Dependencies**: See `requirements.txt`

## License

MIT License
