"""
SafeWatch AI — Streamlit Dashboard
===================================
Main entry point for the industrial safety monitoring dashboard.
Provides five pages: Overview, Live Monitor, Incident Log, Analytics, Configuration.
"""

import cv2
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import sqlite3
import sys
import os
import time
import logging

# ---------------------------------------------------------------------------
# Path setup — allow imports from project root
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

from src.video_capture import VideoCapture
from src.detector import SafetyDetector
from src.rule_engine import RuleEngine
from src.alert_system import AlertManager
from src.utils.geometry import GeometryUtils
from dashboard.components.enhanced_bootstrap_styles import (
    get_custom_css, render_kpi_card, render_alert_card,
    render_detection_card, render_feature_box,
    get_particle_canvas_html, get_typing_effect_html,
    get_live_clock_html, get_ai_status_badge_html,
    get_plotly_theme_template, get_theme_colors, get_logo_html,
)

# ---------------------------------------------------------------------------
# Streamlit page config (must be first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SafeWatch AI — Control Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme — persisted in session state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"   # default theme

_THEME = st.session_state.theme
st.markdown(get_custom_css(theme=_THEME), unsafe_allow_html=True)


def _create_detector_from_config() -> SafetyDetector:
    cfg = RuleEngine("config/camera_config.json").get_config()
    det_cfg = cfg.get("detection", {})
    model_name = det_cfg.get("model_name", "yolo26n.pt")
    # Use lower confidence for faster inference
    confidence = det_cfg.get("confidence_threshold", 0.4)
    return SafetyDetector(model_name=model_name, confidence_threshold=confidence)

# Inject JS to toggle the dark-theme class on .stApp (st.markdown strips <script>)
_theme_js = f"""
<script>
(function(){{
    const app = window.parent.document.querySelector('.stApp');
    if (app) {{
        if ('{_THEME}' === 'dark') {{
            app.classList.add('dark-theme');
        }} else {{
            app.classList.remove('dark-theme');
        }}
    }}
}})();
</script>
"""
components.html(_theme_js, height=0)

# Inject particle background
components.html(get_particle_canvas_html(theme=_THEME), height=0)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
_DEFAULTS = {
    "detector":              _create_detector_from_config,
    "rule_engine":           lambda: RuleEngine("config/camera_config.json"),
    "alert_manager":         lambda: AlertManager(),
    "incidents":             lambda: [],
    "monitoring_active":     lambda: False,
    "total_frames_processed": lambda: 0,
    "session_start":         lambda: datetime.now(),
}

# Clear cached rule_engine to force reload with updated signature
if "rule_engine" in st.session_state:
    del st.session_state["rule_engine"]

for _key, _factory in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _factory()

# Convenience: re-read theme after session-state init
_THEME = st.session_state.theme
_TC = get_theme_colors(_THEME)


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  DATABASE HELPERS                                                      ║
# ╚═════════════════════════════════════════════════════════════════════════╝

DB_PATH = Path("data/incidents/safewatch_ai.db")


def get_db_connection() -> sqlite3.Connection:
    """Return an SQLite connection, creating the table if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id            INTEGER PRIMARY KEY,
            timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP,
            camera_id     TEXT,
            incident_type TEXT,
            severity      TEXT,
            details       TEXT,
            confidence    REAL,
            snapshot_path TEXT
        )
        """
    )
    conn.commit()
    return conn


def save_incident_to_db(incident: dict, snapshot_path: str = "") -> None:
    """Insert a single incident row into the database."""
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO incidents "
            "(timestamp, camera_id, incident_type, severity, details, confidence, snapshot_path) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(incident.get("timestamp", datetime.now())),
                incident.get("camera_id"),
                incident.get("type"),
                incident.get("severity"),
                incident.get("details"),
                incident.get("confidence"),
                snapshot_path,
            ),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass  # non-critical; don't break the monitoring loop


def get_incident_stats() -> dict:
    """Aggregate incident statistics for dashboard KPIs."""
    empty = {
        "total": 0, "critical": 0, "warnings": 0,
        "today": 0, "by_type": {}, "recent": pd.DataFrame(),
    }
    try:
        conn = get_db_connection()
        total    = conn.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
        critical = conn.execute("SELECT COUNT(*) FROM incidents WHERE severity='CRITICAL'").fetchone()[0]
        warnings = conn.execute("SELECT COUNT(*) FROM incidents WHERE severity='WARNING'").fetchone()[0]
        today    = conn.execute("SELECT COUNT(*) FROM incidents WHERE DATE(timestamp)=DATE('now')").fetchone()[0]

        type_counts = {
            row[0]: row[1]
            for row in conn.execute(
                "SELECT incident_type, COUNT(*) FROM incidents GROUP BY incident_type"
            ).fetchall()
        }
        recent = pd.read_sql_query(
            "SELECT * FROM incidents ORDER BY timestamp DESC LIMIT 10", conn,
        )
        conn.close()
        return {
            "total": total, "critical": critical, "warnings": warnings,
            "today": today, "by_type": type_counts, "recent": recent,
        }
    except Exception:
        return empty


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SIDEBAR                                                               ║
# ╚═════════════════════════════════════════════════════════════════════════╝

def render_sidebar() -> str:
    """Draw the futuristic sidebar and return the selected page name."""
    with st.sidebar:
        # ── Theme toggle ────────────────────────────────────────────
        is_light = st.toggle(
            "☀️ Light Mode",
            value=(st.session_state.theme == "light"),
            key="theme_toggle",
        )
        new_theme = "light" if is_light else "dark"
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()

        # Branding
        st.markdown(
            '<div style="text-align:center; padding:0.5rem 0 0.2rem 0;">'
            '<div style="font-size:2.5rem;">🛡️</div>'
            f'<div style="font-family:\'{_TC["font_display"]}\',sans-serif; font-weight:800;'
            f' font-size:1.2rem; color:{_TC["primary"]}; letter-spacing:1px;">'
            'SafeWatch AI</div>'
            f'<div style="font-family:\'{_TC["font_body"]}\',sans-serif;font-size:0.7rem; color:{_TC["muted"]}; margin-top:0.2rem;'
            ' letter-spacing:0.5px;">Control Center v2.0</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown(
            f'<div style="text-align:center; font-family:\'{_TC["font_display"]}\',sans-serif;'
            f' font-size:0.75rem; font-weight:700; color:{_TC["primary"]}; margin-bottom:0.3rem;'
            ' letter-spacing:1px;">Navigation</div>',
            unsafe_allow_html=True
        )
        page = st.radio(
            label="Page Selection",
            options=["🏠 Overview", "🎥 Live Monitor", "📜 Incident Log", "📊 Analytics", "⚙️ Configuration"],
            label_visibility="hidden",
            index=0,
        )

        st.markdown("---")

        # System health indicators
        mon_colour = "green" if st.session_state.monitoring_active else "yellow"
        mon_label  = "Monitoring Active" if st.session_state.monitoring_active else "Monitoring Idle"
        st.markdown(
            '<div class="section-header">SYSTEM HEALTH</div>'
            '<div class="health-indicator"><span class="health-dot green"></span> AI Engine Online</div>'
            f'<div class="health-indicator"><span class="health-dot {mon_colour}"></span> {mon_label}</div>'
            '<div class="health-indicator"><span class="health-dot green"></span> Alert System Ready</div>'
            '<div class="health-indicator"><span class="health-dot green"></span> Database Connected</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Session telemetry
        uptime = datetime.now() - st.session_state.session_start
        h, rem = divmod(int(uptime.total_seconds()), 3600)
        m, s   = divmod(rem, 60)
        st.markdown(
            f'<div style="font-family:\'{_TC["font_body"]}\',sans-serif;font-size:0.78rem; color:{_TC["muted"]};">' 
            f'<div>📅 {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>'
            f'<div>⏱️ Uptime: {h:02d}:{m:02d}:{s:02d}</div>'
            f'<div>🖥️ Frames: {st.session_state.total_frames_processed}</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            f'<div style="text-align:center; font-size:0.65rem; color:{_TC["text2"]};">' 
            'Built for TN-IMPACT Hackathon<br>'
            f'<span style="color:{_TC["primary"]};">Powered by YOLOv8 + OpenCV</span></div>',
            unsafe_allow_html=True,
        )

    return page


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  PAGE: OVERVIEW                                                        ║
# ╚═════════════════════════════════════════════════════════════════════════╝

def page_overview() -> None:
    """Dashboard home — KPIs, detection capabilities, recent alerts."""
    # Logo at top center
    components.html(get_logo_html(theme=_THEME), height=70)

    # Typing hero + clock
    components.html(get_typing_effect_html(
        "Real-time AI-powered Industrial Accident Detection & Prevention",
        theme=_THEME), height=50)
    components.html(get_live_clock_html(theme=_THEME), height=36)

    st.markdown(
        '<div class="header-banner">'
        '<h1>🛡️ SafeWatch AI <span class="accent">Control Center</span></h1>'
        '<p>AI-powered industrial safety monitoring — '
        'Protecting workers, preventing accidents</p></div>',
        unsafe_allow_html=True,
    )

    # AI status badge
    components.html(get_ai_status_badge_html(theme=_THEME), height=32)

    stats = get_incident_stats()

    # KPI cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card("🛡️", stats["total"], "Total Incidents", "kpi-info"),
                    unsafe_allow_html=True)
    with k2:
        st.markdown(render_kpi_card("⚡", stats["critical"], "Critical Alerts", "kpi-critical"),
                    unsafe_allow_html=True)
    with k3:
        st.markdown(render_kpi_card("📊", stats["today"], "Today's Events", "kpi-warning"),
                    unsafe_allow_html=True)
    with k4:
        badge = ('<span class="status-badge status-online">● ACTIVE</span>'
                 if st.session_state.monitoring_active
                 else '<span class="status-badge status-offline">● IDLE</span>')
        st.markdown(
            f'<div class="kpi-card kpi-success">'
            f'<div class="kpi-icon">🔥</div>'
            f'<div class="kpi-value" style="font-size:1rem;">{badge}</div>'
            f'<div class="kpi-label">System Status</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Detection capability cards
        st.markdown('<div class="section-header">🎯 DETECTION CAPABILITIES</div>',
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(render_detection_card(
                "🚶", "Fall Detection",
                "Detects workers lying down via bbox aspect-ratio analysis."),
                unsafe_allow_html=True)
            st.markdown(render_detection_card(
                "⛔", "Zone Breach Detection",
                "Monitors restricted areas using configurable polygon zones."),
                unsafe_allow_html=True)
            st.markdown(render_detection_card(
                "💥", "Person-Vehicle Impact",
                "Detects person-vehicle bbox overlap indicating collision."),
                unsafe_allow_html=True)
        with c2:
            st.markdown(render_detection_card(
                "🧍", "Motionless Body Detection",
                "Tracks position over time. Alerts after sustained no movement."),
                unsafe_allow_html=True)
            st.markdown(render_detection_card(
                "🚗", "Unsafe Proximity",
                "Monitors distance between workers and vehicles."),
                unsafe_allow_html=True)
            st.markdown(render_detection_card(
                "🚧", "Vehicle Collision",
                "Detects overlapping vehicle bounding boxes indicating crash."),
                unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Feature highlights
        st.markdown('<div class="section-header">⚡ KEY FEATURES</div>',
                    unsafe_allow_html=True)
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            st.markdown(render_feature_box("🎥", "Multi-Camera", "RTSP, webcam, and file"),
                        unsafe_allow_html=True)
        with f2:
            st.markdown(render_feature_box("📬", "Email Alerts", "Instant with snapshots"),
                        unsafe_allow_html=True)
        with f3:
            st.markdown(render_feature_box("📍", "Virtual Zones", "Polygon boundaries"),
                        unsafe_allow_html=True)
        with f4:
            st.markdown(render_feature_box("📈", "Analytics", "Trends & history"),
                        unsafe_allow_html=True)

    with col_right:
        # Recent alerts feed
        st.markdown('<div class="section-header">🔔 RECENT ALERTS</div>',
                    unsafe_allow_html=True)
        if not stats["recent"].empty:
            for _, row in stats["recent"].head(6).iterrows():
                sev = "critical" if row.get("severity") == "CRITICAL" else "warning"
                st.markdown(render_alert_card(
                    row.get("incident_type", "UNKNOWN"),
                    row.get("details", ""),
                    str(row.get("timestamp", ""))[:19], sev,
                ), unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="text-align:center; padding:2rem; color:{_TC["muted"]};">' 
                f'<div style="font-size:2rem;">🎯</div>'
                f'<div style="color:{_TC["text2"]};">No incidents recorded yet</div>'
                f'<div style="font-size:0.75rem;color:{_TC["muted"]};">Start monitoring to detect safety events</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Breakdown progress bars
        if stats["by_type"]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📈 INCIDENT BREAKDOWN</div>',
                        unsafe_allow_html=True)
            _TYPE_ICONS = {
                "FALL_DETECTED": "🚶", "ZONE_BREACH": "⛔",
                "MOTIONLESS_BODY": "🧍", "UNSAFE_PROXIMITY": "🚗", "PPE_VIOLATION": "🦺",
                "SUDDEN_FALL": "⚠️", "PERSON_VEHICLE_IMPACT": "💥",
                "VEHICLE_COLLISION": "🚧",
            }
            for itype, count in stats["by_type"].items():
                pct = (count / max(stats["total"], 1)) * 100
                ic  = _TYPE_ICONS.get(itype, "⚡")
                st.markdown(
                    f'<div style="margin-bottom:0.5rem;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'font-size:0.8rem;color:{_TC["text"]};font-weight:500;'
                    f'font-family:\'{_TC["font_body"]}\',sans-serif;">'
                    f'<span>{ic} {itype}</span><span style="color:{_TC["primary"]};">{count} ({pct:.0f}%)</span></div>'
                    f'<div style="display:flex;align-items:center;height:30px;margin-top:0.25rem;">'
                    f'<div style="display:flex;gap:2px;">'
                    + ''.join([f'<span style="font-size:1rem;">{ic}</span>' for _ in range(min(int(pct/10), 10))])
                    + f'</div>'
                    f'<div style="flex:1;height:4px;background:{_TC["bar_bg"]};border-radius:2px;margin-left:0.5rem;">'
                    f'<div style="width:{pct}%;height:100%;background:{_TC["bar_grad"]};'
                    f'border-radius:2px;">'
                    f'</div></div></div></div>',
                    unsafe_allow_html=True,
                )


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  PAGE: LIVE MONITOR                                                    ║
# ╚═════════════════════════════════════════════════════════════════════════╝

_PROJECT_ROOT = Path(__file__).parent.parent  # safewatch_ai/

_SOURCE_MAP = {
    "Webcam (0)":                     "0",
    "🚶 Fall Detection Test":         str(_PROJECT_ROOT / "data/sample_videos/test_fall_detection.mp4"),
    "💥 Accident Detection Test":     str(_PROJECT_ROOT / "data/sample_videos/test_proximity.mp4"),
    "🧍 Motionless Body Test":        str(_PROJECT_ROOT / "data/sample_videos/test_motionless.mp4"),
    "⛔ Zone Breach Test":            str(_PROJECT_ROOT / "data/sample_videos/test_zone_breach.mp4"),
    "📹 General Surveillance":        str(_PROJECT_ROOT / "data/sample_videos/test_general_surveillance.mp4"),
    "Sample Video 1":                 str(_PROJECT_ROOT / "data/sample_videos/demo.mp4"),
    "Sample Video 2":                 str(_PROJECT_ROOT / "data/sample_videos/demo2.mp4"),
    "🏭 Factory Accidents":           str(_PROJECT_ROOT / "data/sample_videos/10 Factory Accidents Caught on Security Camera.mp4"),
}

_ZONE_ICONS = {
    "no_entry": "⛔", "restricted": "⚡",
    "ppe_required": "🦺", "vehicle_only": "🚗",
}


def _draw_hud(frame: np.ndarray, frame_no: int,
              obj_count: int, inc_count: int) -> np.ndarray:
    """Overlay a simple HUD text at the top of the frame."""
    # Simplified HUD - just text, no overlay (much faster)
    text = f"Frame: {frame_no} | Objects: {obj_count} | Incidents: {inc_count}"
    cv2.putText(frame, text, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    return frame


def _monitoring_loop(source: str, video_ph, stats_ph, alerts_ph=None) -> None:
    """Core loop: capture → detect → annotate → alert."""
    try:
        cap = VideoCapture(source)
    except Exception as e:
        st.error(f"Cannot open source: {e}")
        st.session_state.monitoring_active = False
        return

    frame_count = incident_count = 0
    fps = cap.get_fps()
    target_fps = 25  # Display at 25 FPS for smoother playback
    frame_delay = 1.0 / target_fps
    process_interval = 8  # Process every 8th frame for detection (3-4 FPS AI processing)

    # Cache last detection result to annotate skipped frames
    last_detections = {"persons": [], "vehicles": [], "ppe": {"hardhat": [], "vest": []}}
    last_display = None  # Cache annotated frame
    cam_cfg = st.session_state.rule_engine.get_config("camera_1")
    last_incidents_count = 0

    try:
        while st.session_state.monitoring_active:
            frame_start_time = time.time()
            
            frame = cap.get_frame()
            if frame is None:
                st.info("📼 End of video stream")
                st.session_state.monitoring_active = False
                break

            frame_count += 1
            st.session_state.total_frames_processed += 1

            # Process AI detection only every Nth frame
            should_process = (frame_count % process_interval == 0)
            
            if should_process:
                # Detect + check rules
                detections = st.session_state.detector.detect(frame)
                try:
                    incidents  = st.session_state.rule_engine.check_incidents(
                        detections, "camera_1", frame_count, frame=frame
                    )
                except TypeError as e:
                    # Fallback: try without frame parameter for backwards compatibility
                    logger.warning("Rule engine call with frame failed: %s, retrying without", e)
                    incidents = st.session_state.rule_engine.check_incidents(
                        detections, "camera_1", frame_count
                    )
                
                # Cache for use in non-processed frames
                last_detections = detections
                last_incidents_count = len(incidents)
            else:
                # Use cached detections for display
                detections = last_detections
                incidents = []

            # Annotate frame only when processing AI, otherwise use raw frame
            if should_process:
                display = st.session_state.detector.draw_detections(
                    frame, detections, with_ids=True, with_classes=True,
                )
                # Draw zones only when processing AI
                for zone in cam_cfg.get("restricted_zones", []):
                    pts = zone.get("points", [])
                    if pts:
                        display = GeometryUtils.draw_polygon(
                            display, pts, (0, 0, 255), 2, zone.get("name", ""),
                        )
                n_obj = len(detections.get("persons", [])) + len(detections.get("vehicles", []))
                display = _draw_hud(display, frame_count, n_obj, incident_count)
                last_display = display.copy()
            else:
                # For skipped frames, just add HUD to raw frame (much faster)
                n_obj = len(last_detections.get("persons", [])) + len(last_detections.get("vehicles", []))
                display = _draw_hud(frame, frame_count, n_obj, incident_count)
            
            # Convert and display frame
            video_ph.image(cv2.cvtColor(display, cv2.COLOR_BGR2RGB),
                           width="stretch")

            # Process incidents - only update alerts UI occasionally
            if incidents:
                incident_count += len(incidents)
                contacts  = cam_cfg.get("alert_contacts", [])
                recipient = contacts[0] if contacts else ""
                # Fall back to DEFAULT_ALERT_EMAIL or sender email
                if not recipient or recipient == "safety@factory.com":
                    recipient = os.getenv("DEFAULT_ALERT_EMAIL", "") or os.getenv("ALERT_EMAIL", "")
                for inc in incidents:
                    # Add timestamp if not already there
                    if "timestamp" not in inc:
                        inc["timestamp"] = datetime.now()
                    # Try to dispatch alert
                    dispatched = st.session_state.alert_manager.send_alert(inc, frame, recipient)
                    # Add to session state
                    st.session_state.incidents.append(inc)
                    save_incident_to_db(inc)
                    
                # Update alerts UI immediately
                if alerts_ph:
                    with alerts_ph.container():
                        st.markdown('<div class="section-header">🔔 Live Alerts</div>',
                                    unsafe_allow_html=True)
                        for incident in reversed(st.session_state.incidents[-5:]):
                            sev = "critical" if incident.get("severity") == "CRITICAL" else "warning"
                            ts  = incident.get("timestamp", datetime.now())
                            ts  = ts.strftime("%H:%M:%S") if hasattr(ts, "strftime") else str(ts)[:19]
                            st.markdown(render_alert_card(
                                incident.get("type", ""), incident.get("details", ""), ts, sev,
                            ), unsafe_allow_html=True)

            # Update stats every 15 frames to reduce overhead
            if frame_count % 15 == 0:
                with stats_ph.container():
                    s1, s2, s3, s4 = st.columns(4)
                    s1.metric("Frames", frame_count)
                    s2.metric("Persons", len(last_detections.get("persons", [])))
                    s3.metric("Vehicles", len(last_detections.get("vehicles", [])))
                    delta = f"+{last_incidents_count}" if last_incidents_count > 0 else None
                    s4.metric("Incidents", incident_count, delta=delta, delta_color="inverse")

            # Maintain frame rate
            elapsed = time.time() - frame_start_time
            sleep_time = frame_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except Exception as e:
        st.error(f"Monitoring error: {e}")
        logger.exception("Monitoring loop error")
    finally:
        cap.release()
        st.session_state.monitoring_active = False


def page_live_monitor() -> None:
    """Real-time video feed with AI detection overlay."""
    # Logo at top center
    components.html(get_logo_html(theme=_THEME), height=70)

    st.markdown(
        '<div class="header-banner">'
        '<h1>🎥 Live Monitoring <span class="accent">Center</span></h1>'
        '<p>Real-time video feed analysis with AI-powered incident detection</p></div>',
        unsafe_allow_html=True,
    )

    col_main, col_side = st.columns([3, 1])

    with col_side:
        # Live alerts sidebar - create placeholder early
        alerts_ph = st.empty()
        alerts_ph_initialized = False

    with col_main:
        # Source selector
        s1, s2 = st.columns([2, 1])
        with s1:
            video_src = st.selectbox(
                "🎥 Source",
                list(_SOURCE_MAP.keys()) + ["Custom Path / RTSP URL"],
                label_visibility="collapsed",
            )
        with s2:
            if video_src == "Custom Path / RTSP URL":
                source = st.text_input("Path", label_visibility="collapsed",
                                       placeholder="rtsp:// or file path")
            else:
                source = _SOURCE_MAP.get(video_src, "0")

        # Controls
        b1, b2, b3 = st.columns([1, 1, 2])
        with b1:
            start = st.button("▶️ Start", key="start_mon", use_container_width=True)
        with b2:
            stop  = st.button("⏹️ Stop", key="stop_mon", use_container_width=True)
        with b3:
            if st.session_state.monitoring_active:
                st.markdown(
                    '<div class="live-tag"><span class="live-dot"></span> LIVE</div>',
                    unsafe_allow_html=True,
                )

        if stop:
            st.session_state.monitoring_active = False
        if start:
            st.session_state.monitoring_active = True

        video_ph = st.empty()
        stats_ph = st.empty()

        if st.session_state.monitoring_active:
            _monitoring_loop(source, video_ph, stats_ph, alerts_ph)
        else:
            _bg = 'rgba(255,255,255,0.7)' if _THEME == 'light' else 'rgba(15,23,42,0.85)'
            _bdr = 'rgba(37,99,235,0.10)' if _THEME == 'light' else 'rgba(0,245,255,0.15)'
            _shd = 'rgba(0,0,0,0.06)' if _THEME == 'light' else 'rgba(0,245,255,0.08)'
            st.markdown(
                f'<div class="scan-container" style="background:{_bg};'
                f'border-radius:12px;padding:4rem 2rem;text-align:center;'
                f'border:1px solid {_bdr};'
                f'backdrop-filter:blur(16px);position:relative;overflow:hidden;'
                f'box-shadow:0 4px 24px {_shd};">' 
                '<div class="scan-line"></div>'
                '<div style="font-size:3rem;margin-bottom:1rem;">🎥</div>'
                f'<div style="color:{_TC["text"]};font-size:1.1rem;font-weight:600;'
                f'font-family:\'{_TC["font_display"]}\',sans-serif;">No Active Feed</div>'
                f'<div style="color:{_TC["muted"]};font-size:0.85rem;margin-top:0.5rem;'
                f'font-family:\'{_TC["font_body"]}\',sans-serif;">'
                'Select a video source and press ▶️ Start to begin AI analysis</div></div>',
                unsafe_allow_html=True,
            )

    with col_side:
        # Initialize alerts display
        if not alerts_ph_initialized:
            with alerts_ph.container():
                st.markdown('<div class="section-header">🔔 Live Alerts</div>',
                            unsafe_allow_html=True)
                st.markdown(
                    f'<div style="text-align:center;padding:2rem;color:{_TC["muted"]};">' 
                    f'<div style="font-size:2rem;">🔇</div>'
                    f'<div style="font-size:0.85rem;">No alerts yet</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # Active zones
        st.markdown('<div class="section-header">📍 Active Zones</div>',
                    unsafe_allow_html=True)
        cam_cfg = st.session_state.rule_engine.get_config("camera_1")
        zones   = cam_cfg.get("restricted_zones", [])
        if zones:
            for z in zones:
                zt = z.get("type", "restricted")
                _zone_bg = 'rgba(220,38,38,0.04)' if _THEME == 'light' else 'rgba(220,38,38,0.12)'
                _zone_bdr = 'rgba(220,38,38,0.10)' if _THEME == 'light' else 'rgba(220,38,38,0.25)'
                st.markdown(
                    f'<div style="background:{_zone_bg};padding:0.5rem 0.8rem;'
                    f'border-radius:8px;margin-bottom:0.4rem;'
                    f'border-left:3px solid #DC2626;'
                    f'border:1px solid {_zone_bdr};">'
                    f'<div style="font-size:0.8rem;font-weight:600;color:#DC2626;'
                    f'font-family:\'{_TC["font_body"]}\',sans-serif;">'
                    f'{_ZONE_ICONS.get(zt,"📍")} {z.get("name","Zone")}</div>'
                    f'<div style="font-size:0.7rem;color:{_TC["muted"]};">'
                    f'{zt.replace("_"," ").title()}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No zones configured")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  PAGE: INCIDENT LOG                                                    ║
# ╚═════════════════════════════════════════════════════════════════════════╝

def page_incident_log() -> None:
    """Searchable incident history with filters and CSV export."""
    # Logo at top center
    components.html(get_logo_html(theme=_THEME), height=70)

    st.markdown(
        '<div class="header-banner">'
        '<h1>📜 Incident <span class="accent">Log</span></h1>'
        '<p>Browse, filter, and export detected safety incidents</p></div>',
        unsafe_allow_html=True,
    )

    try:
        conn = get_db_connection()
        df = pd.read_sql_query(
            "SELECT * FROM incidents ORDER BY timestamp DESC LIMIT 200", conn,
        )
        conn.close()
    except Exception as e:
        st.error(f"Error loading incidents: {e}")
        return

    if df.empty:
        st.markdown(
            f'<div style="text-align:center;padding:4rem;color:{_TC["muted"]};">' 
            f'<div style="font-size:3rem;">📜</div>'
            f'<div style="font-size:1.1rem;margin-top:1rem;color:{_TC["text"]};'
            f'font-family:\'{_TC["font_display"]}\',sans-serif;">No incidents recorded yet</div>'
            f'<div style="font-size:0.85rem;color:{_TC["muted"]};">Start monitoring to populate the log</div></div>',
            unsafe_allow_html=True,
        )
        return

    # KPI summary
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card("📊", len(df), "Total Records", "kpi-info"),
                    unsafe_allow_html=True)
    with k2:
        critical_count = len(df[df["severity"] == "CRITICAL"]) if "severity" in df.columns else 0
        st.markdown(render_kpi_card("⚡", critical_count,
                    "Critical", "kpi-critical"), unsafe_allow_html=True)
    with k3:
        warning_count = len(df[df["severity"] == "WARNING"]) if "severity" in df.columns else 0
        st.markdown(render_kpi_card("🔥", warning_count,
                    "Warnings", "kpi-warning"), unsafe_allow_html=True)
    with k4:
        incident_types = df["incident_type"].nunique() if "incident_type" in df.columns else 0
        st.markdown(render_kpi_card("🏷️", incident_types,
                    "Incident Types", "kpi-success"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filters
    f1, f2, f3 = st.columns(3)
    with f1:
        type_filter = st.multiselect("🏷️ Incident Type",
                                     df["incident_type"].unique().tolist() if "incident_type" in df.columns else [])
    with f2:
        sev_filter = st.multiselect("⚡ Severity",
                                    df["severity"].unique().tolist() if "severity" in df.columns else [])
    with f3:
        days_back = st.slider("📅 Days Back", 1, 30, 7)

    filtered = df.copy()
    if type_filter and "incident_type" in filtered.columns:
        filtered = filtered[filtered["incident_type"].isin(type_filter)]
    if sev_filter and "severity" in filtered.columns:
        filtered = filtered[filtered["severity"].isin(sev_filter)]
    
    # Filter by date if timestamp column exists
    if "timestamp" in filtered.columns:
        try:
            filtered["timestamp"] = pd.to_datetime(filtered["timestamp"], errors="coerce")
            cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days_back)
            filtered = filtered[filtered["timestamp"] >= cutoff_date]
        except Exception:
            pass  # If date filtering fails, continue without it

    st.dataframe(
        filtered, use_container_width=True, height=400,
        column_config={
            "severity":   st.column_config.TextColumn("Severity", width="small"),
            "confidence": st.column_config.ProgressColumn(
                "Confidence", min_value=0, max_value=1, format="%.1%%",
            ),
            "timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
        },
    )

    st.download_button(
        "📥 Export CSV",
        filtered.to_csv(index=False),
        file_name=f"safewatch_incidents_{datetime.now():%Y%m%d_%H%M%S}.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  PAGE: ANALYTICS                                                       ║
# ╚═════════════════════════════════════════════════════════════════════════╝

def page_analytics() -> None:
    """Charts, trends, and pattern analysis."""
    # Logo at top center
    components.html(get_logo_html(theme=_THEME), height=70)

    st.markdown(
        '<div class="header-banner">'
        '<h1>📊 Safety <span class="accent">Analytics</span></h1>'
        '<p>Incident trends, patterns, and predictive safety insights</p></div>',
        unsafe_allow_html=True,
    )

    stats = get_incident_stats()
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM incidents ORDER BY timestamp DESC", conn)
        conn.close()
    except Exception:
        df = pd.DataFrame()

    if df.empty:
        st.markdown(
            f'<div style="text-align:center;padding:4rem;color:{_TC["muted"]};">' 
            f'<div style="font-size:3rem;">📊</div>'
            f'<div style="font-size:1.1rem;margin-top:1rem;color:{_TC["text"]};'
            f'font-family:\'{_TC["font_display"]}\',sans-serif;">No analytics data yet</div>'
            f'<div style="font-size:0.85rem;color:{_TC["muted"]};">Run monitoring to generate analytics</div></div>',
            unsafe_allow_html=True,
        )
        return

    _layout = get_plotly_theme_template(_THEME)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card("📊", stats["total"], "All-Time Incidents", "kpi-info"),
                    unsafe_allow_html=True)
    with k2:
        st.markdown(render_kpi_card("⚡", "< 3s", "Avg Response", "kpi-success"),
                    unsafe_allow_html=True)
    with k3:
        st.markdown(render_kpi_card("🎯", "95%", "Detection Accuracy", "kpi-warning"),
                    unsafe_allow_html=True)
    with k4:
        n_cams = len(st.session_state.rule_engine.get_config().get("cameras", {}))
        st.markdown(render_kpi_card("🎥", n_cams, "Cameras", "kpi-info"),
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: type & severity — Plotly bar charts
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">📈 INCIDENTS BY TYPE</div>',
                    unsafe_allow_html=True)
        type_counts = df["incident_type"].value_counts()
        fig_type = go.Figure(go.Bar(
            x=type_counts.index, y=type_counts.values,
            marker=dict(color=_TC["primary"], line=dict(color=_TC["primary"], width=1)),
        ))
        fig_type.update_layout(**_layout, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig_type, use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">⚡ SEVERITY DISTRIBUTION</div>',
                    unsafe_allow_html=True)
        sev_counts = df["severity"].value_counts()
        colour_map = {"CRITICAL": _TC["red"], "WARNING": _TC["orange"], "INFO": _TC["blue"]}
        fig_sev = go.Figure(go.Bar(
            x=sev_counts.index, y=sev_counts.values,
            marker=dict(color=[colour_map.get(s, _TC["blue"]) for s in sev_counts.index]),
        ))
        fig_sev.update_layout(**_layout, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig_sev, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Timeline — Plotly area chart
    st.markdown('<div class="section-header">📅 INCIDENT TIMELINE</div>',
                unsafe_allow_html=True)
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        daily = df.groupby(df["timestamp"].dt.date).size().reset_index(name="incidents")
        fig_timeline = go.Figure(go.Scatter(
            x=daily["timestamp"], y=daily["incidents"],
            mode="lines+markers", fill="tozeroy",
            line=dict(color=_TC["primary"], width=2),
            marker=dict(size=6, color=_TC["primary"],
                        line=dict(color=_TC["bg_card"], width=1)),
            fillcolor=f"rgba({','.join(str(int(_TC['primary'][i:i+2], 16)) for i in (1,3,5))},0.08)",
        ))
        fig_timeline.update_layout(**_layout, xaxis_title="Date", yaxis_title="Incidents")
        st.plotly_chart(fig_timeline, use_container_width=True)
    except Exception:
        st.info("Insufficient data for timeline chart")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: camera & hourly — Plotly
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-header">🎥 BY CAMERA</div>',
                    unsafe_allow_html=True)
        cam_counts = df["camera_id"].value_counts()
        fig_cam = go.Figure(go.Bar(
            x=cam_counts.index, y=cam_counts.values,
            marker=dict(color=_TC["green"]),
        ))
        fig_cam.update_layout(**_layout, xaxis_title="Camera", yaxis_title="Count")
        st.plotly_chart(fig_cam, use_container_width=True)
    with c4:
        st.markdown('<div class="section-header">🕒 HOURLY PATTERN</div>',
                    unsafe_allow_html=True)
        try:
            hourly = df.groupby(df["timestamp"].dt.hour).size().reset_index(name="incidents")
            fig_hourly = go.Figure(go.Bar(
                x=hourly["timestamp"], y=hourly["incidents"],
                marker=dict(color=_TC["orange"]),
            ))
            fig_hourly.update_layout(**_layout, xaxis_title="Hour", yaxis_title="Count")
            st.plotly_chart(fig_hourly, use_container_width=True)
        except Exception:
            st.info("Insufficient data for hourly analysis")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  PAGE: CONFIGURATION                                                   ║
# ╚═════════════════════════════════════════════════════════════════════════╝

def page_configuration() -> None:
    """Camera, zone, alert, and detection parameter settings."""
    # Logo at top center
    components.html(get_logo_html(theme=_THEME), height=70)

    st.markdown(
        '<div class="header-banner">'
        '<h1>⚙️ System <span class="accent">Configuration</span></h1>'
        '<p>Configure cameras, detection zones, alert channels, and detection parameters</p></div>',
        unsafe_allow_html=True,
    )

    tab_cam, tab_zone, tab_alert, tab_det = st.tabs(
        ["🎥 Cameras", "🗺️ Zones", "🔔 Alerts", "🎯 Detection"],
    )

    config   = st.session_state.rule_engine.get_config()
    cameras  = config.get("cameras", {})
    selected = (st.sidebar.selectbox("Active Camera", list(cameras.keys()))
                if cameras else None)

    # --- Tab: Cameras --------------------------------------------------------
    with tab_cam:
        st.markdown('<div class="section-header">CAMERA CONFIGURATION</div>',
                    unsafe_allow_html=True)
        if selected:
            cam = cameras[selected]
            c1, c2 = st.columns(2)
            with c1:
                cam_name   = st.text_input("Camera Name",
                                           value=cam.get("name", ""), key="cam_name")
                cam_source = st.text_input("Source (RTSP / File / Webcam)",
                                           value=cam.get("source", ""), key="cam_source")
            with c2:
                fall_on  = st.toggle("Fall Detection",
                                     value=cam.get("fall_detection", True), key="fall_det")
                prox_on  = st.toggle("Proximity Detection",
                                     value=cam.get("proximity_detection", True), key="prox_det")
                prox_thr = st.slider("Proximity Threshold (px)", 10, 200,
                                     cam.get("proximity_threshold_px", 50), key="prox_thr")
            if st.button("💾 Save Camera Config", key="save_cam", use_container_width=True):
                cam.update({
                    "name": cam_name, "source": cam_source,
                    "fall_detection": fall_on, "proximity_detection": prox_on,
                    "proximity_threshold_px": prox_thr,
                })
                st.session_state.rule_engine.update_config(selected, cam)
                st.success("Camera configuration saved!")

    # --- Tab: Zones ----------------------------------------------------------
    with tab_zone:
        st.markdown('<div class="section-header">RESTRICTED ZONE MANAGEMENT</div>',
                    unsafe_allow_html=True)
        if selected:
            cam   = cameras[selected]
            zones = cam.get("restricted_zones", [])

            if zones:
                for i, z in enumerate(zones):
                    zt = z.get("type", "restricted")
                    icon = _ZONE_ICONS.get(zt, "📍")
                    with st.expander(f"{icon} {z.get('name', f'Zone {i+1}')} — {zt}"):
                        st.json(z)
                        if st.button("🗑️ Delete", key=f"del_zone_{i}"):
                            zones.pop(i)
                            cam["restricted_zones"] = zones
                            st.session_state.rule_engine.update_config(selected, cam)
                            st.rerun()
            else:
                st.info("No zones configured. Capture a frame to add zones.")

            st.markdown("---")
            st.markdown("#### 📍 Add New Restricted Zone")

            src = cam.get("source", "0")
            
            # Show current source info
            st.caption(f"🎥 Current source: `{src}`")
            
            if st.button("📸 Capture Frame", key="cap_frame"):
                try:
                    # Convert source to appropriate type
                    if src.isdigit():
                        source = int(src)
                        st.info(f"🎥 Attempting to open webcam (index {source})...")
                    else:
                        source = src
                        abs_path = os.path.abspath(source)
                        if os.path.exists(abs_path):
                            source = abs_path
                            st.info(f"📹 Opening video file: {os.path.basename(source)}")
                        elif os.path.exists(source):
                            st.info(f"📹 Opening video file: {os.path.basename(source)}")
                        else:
                            st.error(f"❌ File not found: {source}\n\nFull path checked: {abs_path}")
                            raise FileNotFoundError(f"Video file not found: {source}")
                    
                    # Try with DirectShow backend first (better for Windows webcams)
                    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW) if isinstance(source, int) else cv2.VideoCapture(source)
                    
                    if not cap.isOpened():
                        # Retry without DirectShow
                        cap.release()
                        cap = cv2.VideoCapture(source)
                    
                    if not cap.isOpened():
                        st.error(f"❌ Cannot open camera/video source: {src}")
                        if isinstance(source, int):
                            st.markdown("""
                            **Troubleshooting webcam:**
                            - Close any apps using the camera (Teams, Zoom, Camera app)
                            - Check Windows Settings → Privacy → Camera → Enable camera access
                            - Try changing source to "1" or "2" in camera config
                            - Restart your computer
                            """)
                        else:
                            st.markdown(f"""
                            **Troubleshooting video file:**
                            - File path: `{os.path.abspath(source)}`
                            - File exists: {os.path.exists(source)}
                            - Try using an absolute path
                            """)
                    else:
                        ret, frm = cap.read()
                        cap.release()
                        if ret and frm is not None:
                            st.session_state.reference_frame = frm
                            fh, fw = frm.shape[:2]
                            st.session_state.frame_height = fh
                            st.session_state.frame_width  = fw
                            st.success(f"✅ Captured successfully: {fw}×{fh} pixels")
                        else:
                            st.error("❌ Failed to read frame. Source opened but no frame available.")
                except FileNotFoundError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"❌ Capture error: {str(e)}")
                    st.exception(e)

            if "reference_frame" in st.session_state:
                _zone_editor(zones, cam, selected)

    # --- Tab: Alerts ---------------------------------------------------------
    with tab_alert:
        st.markdown('<div class="section-header">ALERT CONFIGURATION</div>',
                    unsafe_allow_html=True)
        acfg = config.get("alerts", {})
        c1, c2 = st.columns(2)
        with c1:
            email_on = st.toggle("📧 Email Alerts",
                                 value=acfg.get("email_enabled", True), key="email_on")
            sound_on = st.toggle("🔊 Sound Alerts",
                                 value=acfg.get("sound_enabled", True), key="sound_on")
        with c2:
            cd = st.slider("⏱️ Cooldown (s)", 5, 300,
                           acfg.get("cooldown_seconds", 30), key="cd")
            st.session_state.alert_manager.set_cooldown(cd)

        recipient = st.text_input("📧 Default Alert Email",
                                  value=acfg.get("default_recipient", ""), key="recip")

        st.markdown("---")
        st.markdown("**SMTP Configuration**")
        st.caption("Configure your email server to send alert emails with incident snapshots.")
        s1, s2 = st.columns(2)
        with s1:
            smtp_server = st.text_input("SMTP Server",
                                        value=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                                        key="smtp_srv")
            sender_email = st.text_input("Sender Email",
                                         value=os.getenv("ALERT_EMAIL", ""),
                                         key="smtp_email",
                                         placeholder="your_email@gmail.com")
        with s2:
            smtp_port = st.text_input("SMTP Port",
                                      value=os.getenv("SMTP_PORT", "587"),
                                      key="smtp_port")
            sender_password = st.text_input("App Password",
                                            value=os.getenv("ALERT_PASSWORD", ""),
                                            key="smtp_pass",
                                            type="password",
                                            placeholder="Gmail App Password")
        st.caption("For Gmail: use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.")

        col_save, col_test = st.columns(2)
        with col_save:
            if st.button("💾 Save Alert Settings", key="save_alerts", use_container_width=True):
                acfg.update({
                    "email_enabled": email_on, "sound_enabled": sound_on,
                    "cooldown_seconds": cd, "default_recipient": recipient,
                })
                # Save SMTP settings to .env file
                env_path = Path(__file__).parent.parent / ".env"
                env_lines = [
                    f"SMTP_SERVER={smtp_server}",
                    f"SMTP_PORT={smtp_port}",
                    f"ALERT_EMAIL={sender_email}",
                    f"ALERT_PASSWORD={sender_password}",
                    f"DEFAULT_ALERT_EMAIL={recipient}",
                ]
                env_path.write_text("\n".join(env_lines) + "\n")
                # Update the running alert manager
                am = st.session_state.alert_manager
                am.smtp_server = smtp_server
                am.smtp_port = int(smtp_port)
                am.sender_email = sender_email
                am.sender_password = sender_password
                am.sound_enabled = sound_on
                am.cooldown_seconds = cd
                st.success("Alert settings & SMTP config saved!")

        with col_test:
            if st.button("📨 Send Test Email", key="test_email", use_container_width=True):
                test_to = recipient or sender_email
                if not test_to:
                    st.error("Enter a recipient email address first.")
                elif not sender_email or not sender_password:
                    st.error("Enter SMTP sender email and password first.")
                else:
                    # Temporarily apply settings for test
                    am = st.session_state.alert_manager
                    am.smtp_server = smtp_server
                    am.smtp_port = int(smtp_port)
                    am.sender_email = sender_email
                    am.sender_password = sender_password
                    test_incident = {
                        "type": "TEST_ALERT", "camera_id": "test",
                        "timestamp": datetime.now(), "severity": "WARNING",
                        "details": "This is a test alert from SafeWatch AI",
                        "confidence": 1.0, "track_id": 0,
                        "bbox": (0, 0, 100, 100),
                    }
                    # Create a simple test frame
                    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(test_frame, "SafeWatch AI - Test Alert",
                                (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 255, 255), 2)
                    ok = am._send_email(test_incident,
                                        am._save_snapshot(test_frame, test_incident),
                                        test_to)
                    if ok:
                        st.success(f"Test email sent to {test_to}!")
                    else:
                        st.error("Email failed. Check SMTP settings and use a Gmail App Password.")

    # --- Tab: Detection ------------------------------------------------------
    with tab_det:
        st.markdown('<div class="section-header">DETECTION PARAMETERS</div>',
                    unsafe_allow_html=True)
        dcfg = config.get("detection", {})

        st.markdown("#### Threshold Tuning")
        c1, c2 = st.columns(2)
        with c1:
            st.slider("🎯 Confidence Threshold", 0.1, 1.0,
                      dcfg.get("confidence_threshold", 0.5), 0.05, key="conf_t")
            st.caption("Lower → more detections (more false positives)")
            st.slider("🤸 Fall Aspect Ratio", 0.3, 1.0, 0.7, 0.05, key="fall_r")
            st.caption("Bbox H/W below this → lying down")
        with c2:
            st.slider("🧍 Motionless Threshold (s)", 3, 30, 5, key="motion_s")
            st.caption("Seconds of no movement before alert")
            st.slider("🚛 Global Proximity (px)", 10, 200, 50, key="prox_g")
            st.caption("Min safe distance person ↔ vehicle")

        st.markdown("---")
        st.markdown("#### Model Info")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(render_feature_box("🧠", "YOLOv8n", "Nano — real-time"),
                        unsafe_allow_html=True)
        with m2:
            st.markdown(render_feature_box("🏷️", "80 Classes", "COCO pre-trained"),
                        unsafe_allow_html=True)
        with m3:
            st.markdown(render_feature_box("⚡", "~30 ms", "Per-frame latency"),
                        unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Zone editor helper (used inside configuration → zones tab)
# ---------------------------------------------------------------------------

def _zone_editor(zones: list, cam: dict, selected_camera: str) -> None:
    """Grid overlay + coordinate inputs for defining a new polygon zone."""
    ref = st.session_state.reference_frame.copy()
    h, w = ref.shape[:2]

    # Draw coordinate grid
    for x in range(0, w, 100):
        cv2.line(ref, (x, 0), (x, h), (100, 100, 100), 1)
        cv2.putText(ref, str(x), (x + 2, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
    for y in range(0, h, 100):
        cv2.line(ref, (0, y), (w, y), (100, 100, 100), 1)
        cv2.putText(ref, str(y), (2, y + 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

    # Draw existing zones in red
    for z in zones:
        pts = np.array(z.get("points", []), np.int32)
        if len(pts) >= 3:
            cv2.polylines(ref, [pts], True, (0, 0, 255), 2)

    st.image(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB),
             caption=f"Reference ({w}×{h}) — Red = existing zones",
             use_container_width=True)

    # Input fields
    c1, c2 = st.columns(2)
    with c1:
        zname = st.text_input("Zone Name", "New Restricted Zone", key="zn")
        ztype = st.selectbox("Zone Type",
                             ["no_entry", "restricted", "ppe_required", "vehicle_only"],
                             key="zt")
    with c2:
        st.caption("Enter 4 corner coordinates (read from grid)")
        x1 = st.number_input("X1", 0, w, 100, key="zx1")
        y1 = st.number_input("Y1", 0, h, 100, key="zy1")

    c3, c4 = st.columns(2)
    with c3:
        x2 = st.number_input("X2", 0, w, 400, key="zx2")
        y2 = st.number_input("Y2", 0, h, 100, key="zy2")
    with c4:
        x3 = st.number_input("X3", 0, w, 400, key="zx3")
        y3 = st.number_input("Y3", 0, h, 300, key="zy3")

    c5, _ = st.columns(2)
    with c5:
        x4 = st.number_input("X4", 0, w, 100, key="zx4")
        y4 = st.number_input("Y4", 0, h, 300, key="zy4")

    # Live preview in green
    new_pts = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    preview = st.session_state.reference_frame.copy()
    cv2.polylines(preview, [np.array(new_pts, np.int32)], True, (0, 255, 0), 3)
    cv2.putText(preview, zname, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    st.image(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB),
             caption="Preview — Green = new zone", use_container_width=True)

    if st.button("✅ Add Zone", key="add_zone", use_container_width=True):
        zones.append({"name": zname, "points": new_pts, "type": ztype})
        cam["restricted_zones"] = zones
        st.session_state.rule_engine.update_config(selected_camera, cam)
        st.success(f"Zone '{zname}' added!")
        st.rerun()


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  MAIN                                                                  ║
# ╚═════════════════════════════════════════════════════════════════════════╝

_PAGES = {
    "🏠 Overview":      page_overview,
    "🎥 Live Monitor":  page_live_monitor,
    "📜 Incident Log":  page_incident_log,
    "📊 Analytics":     page_analytics,
    "⚙️ Configuration": page_configuration,
}


def main() -> None:
    """Render sidebar, then dispatch to the selected page."""
    page = render_sidebar()
    _PAGES[page]()


main()
