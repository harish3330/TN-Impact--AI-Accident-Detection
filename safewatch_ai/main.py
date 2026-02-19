"""CLI entry point – run SafeWatch AI with an OpenCV display window.

For the web dashboard, use: streamlit run dashboard/app.py
"""

import logging
import sys
from pathlib import Path

import cv2

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.alert_system import AlertManager
from src.detector import SafetyDetector
from src.rule_engine import RuleEngine
from src.utils.geometry import GeometryUtils
from src.video_capture import VideoCapture

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-20s  %(levelname)-7s  %(message)s",
)
logger = logging.getLogger(__name__)

# ── source selection menu ───────────────────────────────────────────

_SOURCES = {
    "1": ("Webcam", "0"),
    "2": ("Sample video 1", "data/sample_videos/demo.mp4"),
    "3": ("Sample video 2", "data/sample_videos/demo2.mp4"),
}


def _choose_source() -> str:
    print("\n" + "=" * 50)
    print("  SafeWatch AI – Industrial Safety Monitor")
    print("=" * 50)
    print("\nVideo source:")
    for k, (label, _) in _SOURCES.items():
        print(f"  {k}. {label}")
    print("  4. Custom file / RTSP URL")

    choice = input("\nChoice (1-4): ").strip()
    if choice in _SOURCES:
        return _SOURCES[choice][1]
    if choice == "4":
        return input("Path or URL: ").strip()
    return "0"


# ── main loop ───────────────────────────────────────────────────────

def main() -> None:
    logger.info("Starting SafeWatch AI …")

    detector = SafetyDetector("yolov8n.pt", confidence_threshold=0.5)
    rule_engine = RuleEngine("config/camera_config.json")
    alert_manager = AlertManager("data/incidents")

    source = _choose_source()
    capture = VideoCapture(source)

    frame_skip = max(1, int(capture.get_fps() / 5))
    frame_n = 0
    proc_n = 0
    incidents_total = 0
    camera_id = "camera_1"

    logger.info("Processing at ~5 FPS (skip=%d). Press 'q' to quit.", frame_skip)

    while True:
        frame = capture.get_frame()
        if frame is None:
            break

        frame_n += 1
        if frame_n % frame_skip != 0:
            continue
        proc_n += 1

        detections = detector.detect(frame)
        incidents = rule_engine.check_incidents(detections, camera_id, proc_n)

        for inc in incidents:
            incidents_total += 1
            logger.info("INCIDENT #%d: %s – %s",
                        incidents_total, inc["type"], inc["details"])
            alert_manager.send_alert(inc, frame)

        # Annotate frame
        display = detector.draw_detections(frame, detections)
        for zone in rule_engine.get_config(camera_id).get("restricted_zones", []):
            pts = zone.get("points", [])
            if pts:
                display = GeometryUtils.draw_polygon(
                    display, pts, (0, 0, 255), 2, zone.get("name", ""))

        cv2.putText(display,
                    f"Frame {proc_n} | Incidents {incidents_total}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("SafeWatch AI", display)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()
    logger.info("Done – %d frames processed, %d incidents.", proc_n, incidents_total)


if __name__ == "__main__":
    main()
