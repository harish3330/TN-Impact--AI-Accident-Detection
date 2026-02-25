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
        FALL_DETECTED          – person lying down (aspect ratio < threshold)
        MOTIONLESS_BODY        – person stationary for extended time
        ZONE_BREACH            – person inside a restricted polygon
        UNSAFE_PROXIMITY       – person too close to a vehicle
        PERSON_VEHICLE_IMPACT  – person bbox overlapping vehicle bbox
        VEHICLE_COLLISION      – two vehicles with high IoU / close proximity
        SUDDEN_FALL            – rapid aspect-ratio drop (upright → horizontal)
        PPE_VIOLATION          – person in PPE-required zone (placeholder)
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
            # Fallback: use first camera config or sensible defaults
            cameras = self.config.get("cameras", {})
            cam = next(iter(cameras.values()), {}) if cameras else {
                "fall_detection": True,
                "proximity_detection": True,
                "proximity_threshold_px": 150,
                "restricted_zones": [],
            }

        persons = detections.get("persons", [])
        vehicles = detections.get("vehicles", [])

        incidents: List[Dict] = []
        incidents += self._check_fall(persons, camera_id, cam)
        incidents += self._check_sudden_fall(persons, camera_id, cam)
        incidents += self._check_motionless(persons, camera_id, cam)
        incidents += self._check_zone_breach(persons, camera_id, frame_idx, cam)
        incidents += self._check_proximity(persons, vehicles, camera_id, cam)
        incidents += self._check_person_vehicle_impact(persons, vehicles, camera_id, cam)
        incidents += self._check_vehicle_collision(vehicles, camera_id, cam)
        incidents += self._check_ppe(persons, camera_id, cam)
        return incidents

    # ── individual checks ───────────────────────────────────────────

    def _check_fall(self, persons: List, camera_id: str,
                    cfg: Dict) -> List[Dict]:
        """Person lying down (height/width < 0.8) for >= required frames."""
        if not cfg.get("fall_detection", True):
            return []

        # Get config values — use lower defaults for easier triggering
        global_config = self.config.get("detection", {})
        aspect_ratio_threshold = global_config.get("fall_aspect_ratio", 0.8)
        required_frames = global_config.get("fall_detection_frames", 4)

        incidents: List[Dict] = []
        for x1, y1, x2, y2, conf, tid in persons:
            ar = GeometryUtils.get_bbox_aspect_ratio((x1, y1, x2, y2))
            # Fall detected when height/width < threshold (person is horizontal)
            is_falling = ar < aspect_ratio_threshold
            self.state_tracker.update_fall_state(tid, is_falling)
            dur = self.state_tracker.get_fall_duration(tid)
            if dur >= required_frames:
                incidents.append(self._incident(
                    "FALL_DETECTED", camera_id, conf, (x1, y1, x2, y2), tid,
                    f"Person lying down for {dur / 5:.1f}s (AR: {ar:.2f})", "CRITICAL",
                    aspect_ratio=ar,
                ))
        return incidents

    def _check_motionless(self, persons: List, camera_id: str,
                          cfg: Dict) -> List[Dict]:
        """Person stationary for >= required frames."""
        if not cfg.get("fall_detection", True):
            return []

        # Get config values — more sensitive defaults
        global_config = self.config.get("detection", {})
        motion_threshold = global_config.get("motionless_threshold_px", 30)
        required_frames = global_config.get("motionless_detection_frames", 10)  # ~2s at 5 FPS

        incidents: List[Dict] = []
        for x1, y1, x2, y2, conf, tid in persons:
            centroid = GeometryUtils.get_centroid((x1, y1, x2, y2))
            dur = self.state_tracker.update_motionless_state(tid, centroid, motion_threshold)
            if dur >= required_frames:
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
        """Person within threshold px of a vehicle for >= required frames."""
        threshold = cfg.get("proximity_threshold_px", 150)
        global_config = self.config.get("detection", {})
        required_frames = global_config.get("proximity_detection_frames", 3)
        
        incidents: List[Dict] = []
        for px1, py1, px2, py2, pconf, pid in persons:
            pc = GeometryUtils.get_centroid((px1, py1, px2, py2))
            for vx1, vy1, vx2, vy2, vconf, vid in vehicles:
                vbox = (vx1, vy1, vx2, vy2)
                dist = GeometryUtils.distance_point_to_bbox(pc, vbox)
                dur = self.state_tracker.update_proximity_state(pid, dist < threshold)
                if dist < threshold and dur >= required_frames:
                    incidents.append(self._incident(
                        "UNSAFE_PROXIMITY", camera_id, min(pconf, vconf),
                        (px1, py1, px2, py2), pid,
                        f"Person too close to vehicle ({dist:.0f}px, {dur / 5:.1f}s)",
                        "WARNING", distance=dist, vehicle_bbox=vbox,
                    ))
        return incidents

    # ── NEW: accident-oriented checks ───────────────────────────────

    def _check_sudden_fall(self, persons: List, camera_id: str,
                           cfg: Dict) -> List[Dict]:
        """Detect rapid transition from upright (AR > 1.2) to lying (AR < 0.8).

        This catches actual falls rather than people who are just short/wide.
        """
        if not cfg.get("fall_detection", True):
            return []
        incidents: List[Dict] = []
        for x1, y1, x2, y2, conf, tid in persons:
            ar = GeometryUtils.get_bbox_aspect_ratio((x1, y1, x2, y2))
            prev_ar, cur_ar = self.state_tracker.update_aspect_ratio(tid, ar)
            if prev_ar is not None:
                # Person went from standing (AR > 1.2) to horizontal (AR < 0.85)
                ar_drop = prev_ar - cur_ar
                if prev_ar > 1.2 and cur_ar < 0.85 and ar_drop > 0.5:
                    incidents.append(self._incident(
                        "SUDDEN_FALL", camera_id, conf, (x1, y1, x2, y2), tid,
                        (f"Sudden fall detected — AR dropped from "
                         f"{prev_ar:.2f} to {cur_ar:.2f}"),
                        "CRITICAL", aspect_ratio=cur_ar, ar_drop=ar_drop,
                    ))
        return incidents

    def _check_person_vehicle_impact(self, persons: List, vehicles: List,
                                     camera_id: str, cfg: Dict) -> List[Dict]:
        """Person bbox overlapping a vehicle bbox → potential impact/accident."""
        global_config = self.config.get("detection", {})
        required_frames = global_config.get("impact_detection_frames", 2)
        iou_threshold = global_config.get("impact_iou_threshold", 0.05)

        incidents: List[Dict] = []
        for px1, py1, px2, py2, pconf, pid in persons:
            pbox = (px1, py1, px2, py2)
            for vx1, vy1, vx2, vy2, vconf, vid in vehicles:
                vbox = (vx1, vy1, vx2, vy2)
                iou = GeometryUtils.bbox_iou(pbox, vbox)
                dur = self.state_tracker.update_impact_state(pid, iou > iou_threshold)
                if iou > iou_threshold and dur >= required_frames:
                    incidents.append(self._incident(
                        "PERSON_VEHICLE_IMPACT", camera_id, min(pconf, vconf),
                        (px1, py1, px2, py2), pid,
                        (f"Person-vehicle collision detected "
                         f"(IoU: {iou:.2f}, {dur / 5:.1f}s)"),
                        "CRITICAL", iou=iou, vehicle_bbox=vbox,
                    ))
        return incidents

    def _check_vehicle_collision(self, vehicles: List, camera_id: str,
                                 cfg: Dict) -> List[Dict]:
        """Two vehicles with overlapping bboxes → potential collision."""
        global_config = self.config.get("detection", {})
        required_frames = global_config.get("collision_detection_frames", 2)
        iou_threshold = global_config.get("collision_iou_threshold", 0.08)

        incidents: List[Dict] = []
        for i, (ax1, ay1, ax2, ay2, aconf, aid) in enumerate(vehicles):
            abox = (ax1, ay1, ax2, ay2)
            for bx1, by1, bx2, by2, bconf, bid in vehicles[i + 1:]:
                bbox_b = (bx1, by1, bx2, by2)
                iou = GeometryUtils.bbox_iou(abox, bbox_b)
                # Also check centroid proximity
                ac = GeometryUtils.get_centroid(abox)
                bc = GeometryUtils.get_centroid(bbox_b)
                dist = GeometryUtils.distance_between_points(ac, bc)
                colliding = iou > iou_threshold or dist < 80
                dur = self.state_tracker.update_collision_state(aid, colliding)
                if colliding and dur >= required_frames:
                    incidents.append(self._incident(
                        "VEHICLE_COLLISION", camera_id, min(aconf, bconf),
                        abox, aid,
                        (f"Vehicle collision detected "
                         f"(IoU: {iou:.2f}, dist: {dist:.0f}px, {dur / 5:.1f}s)"),
                        "CRITICAL", iou=iou, distance=dist,
                        vehicle_b_bbox=bbox_b,
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
