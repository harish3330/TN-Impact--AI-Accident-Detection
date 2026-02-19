"""Rule engine for detecting safety incidents from video detections."""

import json
import logging
from datetime import datetime
from typing import Dict, List

from src.utils.geometry import GeometryUtils
from src.utils.tracking import StateTracker

logger = logging.getLogger(__name__)


class RuleEngine:
    """Evaluate safety rules against per-frame detections.

    Supported incident types:
        FALL_DETECTED    – person lying down (aspect ratio < 0.7) for >= 3 s
        MOTIONLESS_BODY  – person stationary for >= 5 s
        ZONE_BREACH      – person inside a restricted polygon
        UNSAFE_PROXIMITY – person too close to a vehicle for >= 2 s
        PPE_VIOLATION    – person in PPE-required zone (placeholder)
    """

    def __init__(self, config_path: str):
        self.config: Dict = {}
        self.state_tracker = StateTracker()
        self._load_config(config_path)

    # ── configuration ───────────────────────────────────────────────

    def _load_config(self, config_path: str) -> None:
        """Load camera / zone config from *config_path* (JSON)."""
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            logger.info("Config loaded from %s", config_path)
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            logger.warning("Config load failed (%s) – using defaults", exc)
            self.config = {
                "cameras": {
                    "camera_1": {
                        "source": "sample.mp4",
                        "restricted_zones": [],
                        "ppe_required": False,
                        "fall_detection": True,
                        "proximity_threshold": 50,
                    }
                },
                "alerts": {
                    "email": "safety@factory.com",
                    "cooldown_seconds": 30,
                    "sound_enabled": True,
                },
            }

    def get_config(self, camera_id: str | None = None) -> Dict:
        """Return config for one camera, or the full config dict."""
        if camera_id:
            return self.config.get("cameras", {}).get(camera_id, {})
        return self.config

    def update_config(self, camera_id: str, new_config: Dict) -> None:
        """Merge *new_config* for *camera_id* and persist to disk."""
        self.config.setdefault("cameras", {})[camera_id] = new_config
        self.save_config("config/camera_config.json")
        logger.info("Config updated for %s", camera_id)

    def save_config(self, config_path: str) -> None:
        """Write current config to *config_path*."""
        try:
            with open(config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except OSError as exc:
            logger.error("Failed to save config: %s", exc)

    # ── incident dispatcher ─────────────────────────────────────────

    def check_incidents(self, detections: Dict, camera_id: str,
                        frame_idx: int) -> List[Dict]:
        """Run all rule checks and return a list of incident dicts."""
        cam = self.config.get("cameras", {}).get(camera_id, {})
        if not cam:
            return []

        persons = detections.get("persons", [])
        vehicles = detections.get("vehicles", [])

        incidents: List[Dict] = []
        incidents += self._check_fall(persons, camera_id, cam)
        incidents += self._check_motionless(persons, camera_id, cam)
        incidents += self._check_zone_breach(persons, camera_id, frame_idx, cam)
        incidents += self._check_proximity(persons, vehicles, camera_id, cam)
        incidents += self._check_ppe(persons, camera_id, cam)
        return incidents

    # ── individual checks ───────────────────────────────────────────

    def _check_fall(self, persons: List, camera_id: str,
                    cfg: Dict) -> List[Dict]:
        """Person lying down (height/width < 0.7) for >= 15 frames (~3 s)."""
        if not cfg.get("fall_detection", True):
            return []

        incidents: List[Dict] = []
        for x1, y1, x2, y2, conf, tid in persons:
            ar = GeometryUtils.get_bbox_aspect_ratio((x1, y1, x2, y2))
            self.state_tracker.update_fall_state(tid, ar < 0.7)
            dur = self.state_tracker.get_fall_duration(tid)
            if dur >= 15:
                incidents.append(self._incident(
                    "FALL_DETECTED", camera_id, conf, (x1, y1, x2, y2), tid,
                    f"Person lying down for {dur / 5:.1f}s", "CRITICAL",
                    aspect_ratio=ar,
                ))
        return incidents

    def _check_motionless(self, persons: List, camera_id: str,
                          cfg: Dict) -> List[Dict]:
        """Person stationary (< 15 px movement) for >= 25 frames (~5 s)."""
        if not cfg.get("fall_detection", True):
            return []

        incidents: List[Dict] = []
        for x1, y1, x2, y2, conf, tid in persons:
            centroid = GeometryUtils.get_centroid((x1, y1, x2, y2))
            dur = self.state_tracker.update_motionless_state(tid, centroid, 15)
            if dur >= 25:
                incidents.append(self._incident(
                    "MOTIONLESS_BODY", camera_id, conf, (x1, y1, x2, y2), tid,
                    f"Person motionless for {dur / 5:.1f}s", "CRITICAL",
                ))
        return incidents

    def _check_zone_breach(self, persons: List, camera_id: str,
                           frame_idx: int, cfg: Dict) -> List[Dict]:
        """Person centroid inside a restricted polygon."""
        incidents: List[Dict] = []
        for zone in cfg.get("restricted_zones", []):
            pts = zone.get("points", [])
            name = zone.get("name", "Unknown")
            if len(pts) < 3:
                continue
            for x1, y1, x2, y2, conf, tid in persons:
                c = GeometryUtils.get_centroid((x1, y1, x2, y2))
                in_zone = GeometryUtils.point_in_polygon(c, pts)
                self.state_tracker.update_zone_entry(tid, in_zone, frame_idx)
                if in_zone and self.state_tracker.get_zone_entry_frame(tid) is not None:
                    incidents.append(self._incident(
                        "ZONE_BREACH", camera_id, conf, (x1, y1, x2, y2), tid,
                        f"Person entered restricted zone: {name}", "WARNING",
                        zone_name=name, centroid=c,
                    ))
        return incidents

    def _check_proximity(self, persons: List, vehicles: List,
                         camera_id: str, cfg: Dict) -> List[Dict]:
        """Person within *threshold* px of a vehicle for >= 10 frames (~2 s)."""
        threshold = cfg.get("proximity_threshold_px", 50)
        incidents: List[Dict] = []
        for px1, py1, px2, py2, pconf, pid in persons:
            pc = GeometryUtils.get_centroid((px1, py1, px2, py2))
            for vx1, vy1, vx2, vy2, vconf, vid in vehicles:
                vbox = (vx1, vy1, vx2, vy2)
                dist = GeometryUtils.distance_point_to_bbox(pc, vbox)
                dur = self.state_tracker.update_proximity_state(pid, dist < threshold)
                if dist < threshold and dur >= 10:
                    incidents.append(self._incident(
                        "UNSAFE_PROXIMITY", camera_id, min(pconf, vconf),
                        (px1, py1, px2, py2), pid,
                        f"Person too close to vehicle ({dist:.0f}px, {dur / 5:.1f}s)",
                        "WARNING", distance=dist, vehicle_bbox=vbox,
                    ))
        return incidents

    def _check_ppe(self, persons: List, camera_id: str,
                   cfg: Dict) -> List[Dict]:
        """Placeholder – requires a specialised PPE detection model."""
        if not cfg.get("ppe_required", False):
            return []

        zone_map = {
            z.get("name"): z.get("points", [])
            for z in cfg.get("restricted_zones", [])
        }
        incidents: List[Dict] = []
        for zone_name in cfg.get("ppe_required_zones", []):
            pts = zone_map.get(zone_name, [])
            if not pts:
                continue
            for x1, y1, x2, y2, conf, tid in persons:
                c = GeometryUtils.get_centroid((x1, y1, x2, y2))
                if GeometryUtils.point_in_polygon(c, pts):
                    incidents.append(self._incident(
                        "PPE_VIOLATION", camera_id, conf, (x1, y1, x2, y2), tid,
                        f"Person in {zone_name} without proper PPE", "WARNING",
                        zone_name=zone_name,
                    ))
        return incidents

    # ── helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _incident(type_: str, camera_id: str, confidence: float,
                  bbox: tuple, track_id: int, details: str,
                  severity: str, **extra) -> Dict:
        """Build a normalised incident dict."""
        return {
            "type": type_,
            "camera_id": camera_id,
            "timestamp": datetime.now(),
            "confidence": confidence,
            "bbox": bbox,
            "track_id": track_id,
            "details": details,
            "severity": severity,
            **extra,
        }
