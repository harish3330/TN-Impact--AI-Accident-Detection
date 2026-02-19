# SafeWatch AI

Real-time industrial accident detection system powered by YOLOv8.  
Monitors CCTV / webcam feeds, detects safety incidents, and dispatches
multi-channel alerts (email + sound + snapshot).

---

## Features

| Capability | How it works |
|---|---|
| **Fall detection** | Bounding-box aspect ratio < 0.7 sustained for ≥ 3 s |
| **Motionless body** | Centroid movement < 15 px for ≥ 5 s |
| **Zone breach** | Person centroid inside a user-drawn restricted polygon |
| **Unsafe proximity** | Person within threshold distance of a vehicle for ≥ 2 s |
| **PPE violation** | Placeholder – requires a specialised PPE model |
| **Email alerts** | SMTP with annotated snapshot attachment |
| **Sound alerts** | System beep (critical = 3×, warning = 1×) |
| **Incident log** | SQLite database + searchable Streamlit table |
| **Zone editor** | Draw / edit restricted polygons on a live frame |

---

## Quick start

```bash
# 1. Install dependencies (Python 3.10+)
pip install -r requirements.txt

# 2. Copy and edit the environment file
#    For Gmail use an App Password, not your regular password.
cp .env.example .env          # then edit ALERT_EMAIL / ALERT_PASSWORD

# 3. Launch the Streamlit dashboard
streamlit run dashboard/app.py
```

The dashboard opens at **http://localhost:8501**.

> **CLI alternative** – `python main.py` runs the detector with an OpenCV window
> (no browser required).

---

## Project structure

```
safewatch_ai/
├── main.py                     # CLI entry point (OpenCV window)
├── requirements.txt
├── .env                        # SMTP credentials (not committed)
├── yolov8n.pt                  # YOLO nano weights (auto-downloaded)
│
├── config/
│   └── camera_config.json      # Cameras, zones, thresholds
│
├── dashboard/
│   ├── app.py                  # Streamlit app (5 pages)
│   └── components/
│       ├── __init__.py
│       └── styles.py           # CSS theme + HTML card renderers
│
├── src/
│   ├── __init__.py
│   ├── detector.py             # YOLOv8 wrapper + centroid tracker
│   ├── rule_engine.py          # Incident rules (5 check types)
│   ├── alert_system.py         # Email / sound / snapshot dispatcher
│   ├── video_capture.py        # Webcam / RTSP / file abstraction
│   └── utils/
│       ├── __init__.py
│       ├── geometry.py         # Point-in-polygon, IoU, distances
│       └── tracking.py         # ObjectTracker + StateTracker
│
├── data/
│   ├── incidents/              # Snapshots + SQLite DB
│   └── sample_videos/          # Demo footage
│
└── tests/
    └── test_scenarios.py       # pytest suite
```

---

## Configuration

### Camera zones – `config/camera_config.json`

```jsonc
{
  "cameras": {
    "camera_1": {
      "source": "rtsp://admin:pass@192.168.1.100/stream",
      "name": "Manufacturing Floor",
      "fall_detection": true,
      "proximity_threshold_px": 50,
      "restricted_zones": [
        {
          "name": "Machine Area",
          "points": [[100,50],[600,50],[600,400],[100,400]]
        }
      ]
    }
  }
}
```

Zones can also be drawn interactively on the **Configuration** page of the
dashboard.

### Email alerts – `.env`

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
ALERT_EMAIL=you@gmail.com
ALERT_PASSWORD=xxxx xxxx xxxx xxxx   # Gmail App Password
DEFAULT_ALERT_EMAIL=safety@company.com
```

---

## Testing

```bash
pytest tests/test_scenarios.py -v
```

---

## Tech stack

- **Detection** – [Ultralytics YOLOv8](https://docs.ultralytics.com/) (nano)
- **Vision** – OpenCV
- **Dashboard** – Streamlit
- **Database** – SQLite (via `sqlite3`)
- **Alerting** – Python `smtplib` + `email.mime`

---

## License

MIT
