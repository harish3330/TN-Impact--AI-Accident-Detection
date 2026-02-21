# SafeWatch AI - Industrial Safety Monitoring System

🏆 **TN-IMPACT Hackathon Project**

AI-powered real-time industrial safety monitoring system using YOLOv8 for accident detection, fall detection, and zone intrusion monitoring.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Webcam or video source
- Windows/Linux/MacOS

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd TN-Impact--AI-Accident-Detection
```

2. **Create virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/MacOS
source .venv/bin/activate
```

3. **Install dependencies**
```bash
cd safewatch_ai
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run dashboard/app.py
```

5. **Access the dashboard**
- Local: http://localhost:8501
- Network: http://<your-ip>:8501

---

## 📁 Project Structure

```
TN-Impact--AI-Accident-Detection/
│
├── .venv/                          # Virtual environment
├── .gitignore                      # Git ignore rules
│
└── safewatch_ai/                   # Main application package
    │
    ├── main.py                     # CLI entry point
    ├── requirements.txt            # Python dependencies
    ├── README.md                   # Detailed documentation
    ├── yolov8n.pt                  # YOLOv8 model weights
    │
    ├── config/                     # Configuration files
    │   └── camera_config.json      # Camera and zone settings
    │
    ├── src/                        # Core application logic
    │   ├── __init__.py
    │   ├── detector.py             # YOLOv8 detection engine
    │   ├── video_capture.py        # Video/camera capture
    │   ├── rule_engine.py          # Safety rules engine
    │   ├── alert_system.py         # Alert notifications
    │   │
    │   └── utils/                  # Utility modules
    │       ├── __init__.py
    │       ├── geometry.py         # Geometric calculations
    │       └── tracking.py         # Object tracking
    │
    ├── dashboard/                  # Streamlit web interface
    │   ├── app.py                  # Main dashboard application
    │   │
    │   └── components/             # UI components
    │       ├── __init__.py
    │       └── styles.py           # CSS styling
    │
    ├── data/                       # Data storage
    │   ├── incidents/              # Incident logs & database
    │   └── sample_videos/          # Demo videos
    │
    └── tests/                      # Test scenarios
        └── test_scenarios.py
```

---

## 🎯 Features

### 🔍 **Real-Time Detection**
- **Person Detection**: YOLOv8-based human detection
- **Fall Detection**: AI-powered fall incident detection
- **Zone Monitoring**: Restricted area intrusion detection
- **Multi-Camera**: Support for multiple camera feeds

### 📊 **Dashboard Features**
- **Live Monitor**: Real-time video feed with detection overlays
- **KPI Cards**: Active cameras, detections, incidents, alerts
- **Incident Log**: Historical incident database
- **Analytics**: Detection trends and statistics
- **Configuration**: Visual zone editor with coordinate mapping

### 🚨 **Alert System**
- Database logging (SQLite)
- Email notifications (configurable)
- Severity levels: Critical, Warning, Info
- Incident screenshots

### 🎨 **Modern UI**
- Responsive design
- Medium theme with gradient effects
- Animated KPI cards
- Interactive zone editor
- Real-time charts

---

## ⚙️ Configuration

### Camera Setup

Edit `config/camera_config.json`:

```json
{
  "camera_1": {
    "name": "Main Camera",
    "source": "0",              // 0 = webcam, or path to video
    "restricted_zones": [
      [[100, 100], [500, 100], [500, 400], [100, 400]]
    ],
    "enabled_detections": {
      "fall_detection": true,
      "proximity_detection": false,
      "restricted_zone": true
    }
  }
}
```

### Environment Variables

Create `.env` file:

```env
ALERT_EMAIL=your-email@gmail.com
ALERT_PASSWORD=your-app-password
```

---

## 🛠️ Development

### Code Structure

- **src/detector.py**: Core detection logic using Ultralytics YOLOv8
- **src/rule_engine.py**: Safety rule evaluation engine
- **src/video_capture.py**: OpenCV video processing
- **dashboard/app.py**: Streamlit multi-page application
- **dashboard/components/styles.py**: CSS design system

### Adding New Detection Rules

1. Add rule to `src/rule_engine.py`
2. Update `config/camera_config.json` schema
3. Modify UI in `dashboard/app.py`

---

## 📦 Dependencies

- **streamlit**: Web dashboard framework
- **opencv-python**: Video processing
- **ultralytics**: YOLOv8 implementation
- **torch**: Deep learning backend
- **pandas**: Data manipulation
- **numpy**: Numerical operations

---

## 🏆 Hackathon Highlights

- **Real-time AI**: YOLOv8 with 80 COCO classes
- **Production Ready**: Database logging, error handling
- **Scalable**: Multi-camera support
- **Modern UI**: Professional dashboard design
- **Configurable**: Visual zone editor

---

## 📝 License

This project is developed for TN-IMPACT Hackathon.

---

## 👥 Team

Industrial Safety Monitoring System powered by AI

---

## 🤝 Contributing

For hackathon purposes, contributions are managed by the team.

---

## 📧 Contact

For questions or support during the hackathon, contact the team.
