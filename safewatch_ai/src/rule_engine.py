import json
import logging
from datetime import datetime
from typing import Dict, List

import cv2
import numpy as np

from src.utils.geometry import GeometryUtils
from src.utils.tracking import StateTracker

logger = logging.getLogger(__name__)


class RuleEngine:

    def __init__(self, config_path: str):
        self.config: Dict = {}
        self.state_tracker = StateTracker()
        self.prev_frame_brightness = None
        self._load_config(config_path)

    def _load_config(self, config_path: str) -> None:
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            logger.info("Config loaded from %s", config_path)
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            logger.warning("Config load failed (%s) — using defaults", exc)
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
        if camera_id:
            return self.config.get("cameras", {}).get(camera_id, {})
        return self.config

    def update_config(self, camera_id: str, new_config: Dict) -> None:
        self.config.setdefault("cameras", {})[camera_id] = new_config
        self.save_config("config/camera_config.json")
        logger.info("Config updated for %s", camera_id)

    def save_config(self, config_path: str) -> None:
        try:
            with open(config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except OSError as exc:
            logger.error("Failed to save config: %s", exc)

    def check_incidents(self, detections, camera_id, frame_idx, frame=None):
        cam = self.config.get("cameras", {}).get(camera_id, {})
        if not cam:
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

        if frame is not None:
            try:
                incidents += self._check_blast(frame, camera_id)
            except Exception as e:
                logger.warning("Blast detection failed: %s", e)
            try:
                incidents += self._check_fire(frame, camera_id)
            except Exception as e:
                logger.warning("Fire detection failed: %s", e)

        return incidents

    def _check_fall(self, persons: List, camera_id: str, cfg: Dict) -> List[Dict]:
        if not cfg.get("fall_detection", True):
            return []

        global_config = self.config.get("detection", {})
        aspect_ratio_threshold = global_config.get("fall_aspect_ratio", 0.8)
        required_frames = global_config.get("fall_detection_frames", 4)
        min_person_bbox_area = global_config.get("min_person_bbox_area", 12000)
        min_confidence = global_config.get("fall_min_confidence", 0.5)

        incidents: List[Dict] = []
        for x1, y1, x2, y2, conf, tid in persons:
            bbox = (x1, y1, x2, y2)
            if conf < min_confidence:
                self.state_tracker.update_fall_state(tid, False)
                continue
            if GeometryUtils.get_bbox_area(bbox) < min_person_bbox_area:
                self.state_tracker.update_fall_state(tid, False)
                continue
            ar = GeometryUtils.get_bbox_aspect_ratio(bbox)
            is_falling = ar < aspect_ratio_threshold
            self.state_tracker.update_fall_state(tid, is_falling)
            dur = self.state_tracker.get_fall_duration(tid)
            if dur >= required_frames:
                incidents.append(self._incident(
                    "FALL_DETECTED", camera_id, conf, bbox, tid,
                    f"Person lying down for {dur / 5:.1f}s (AR: {ar:.2f})", "CRITICAL",
                    aspect_ratio=ar,
                ))
        return incidents

    def _check_motionless(self, persons: List, camera_id: str, cfg: Dict) -> List[Dict]:
        if not cfg.get("fall_detection", True):
            return []

        global_config = self.config.get("detection", {})
        motion_threshold = global_config.get("motionless_threshold_px", 30)
        required_frames = global_config.get("motionless_detection_frames", 10)

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
        incidents: List[Dict] = []
        for zone in cfg.get("restricted_zones", []):
            pts = zone.get("points", [])
            name = zone.get("name", "Unknown")
            if len(pts) < 3:
                continue
            for x1, y1, x2, y2, conf, tid in persons:
                c = GeometryUtils.get_centroid((x1, y1, x2, y2))
                in_zone = GeometryUtils.point_in_polygon(c, pts)
                prev_entry = self.state_tracker.get_zone_entry_frame(tid)
                self.state_tracker.update_zone_entry(tid, in_zone, frame_idx)
                if in_zone and prev_entry is None:
                    incidents.append(self._incident(
                        "ZONE_BREACH", camera_id, conf, (x1, y1, x2, y2), tid,
                        f"Person entered restricted zone: {name}", "WARNING",
                        zone_name=name, centroid=c,
                    ))
        return incidents

    def _check_proximity(self, persons: List, vehicles: List,
                         camera_id: str, cfg: Dict) -> List[Dict]:
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

    def _check_sudden_fall(self, persons: List, camera_id: str, cfg: Dict) -> List[Dict]:
        if not cfg.get("fall_detection", True):
            return []
        global_config = self.config.get("detection", {})
        prev_ar_min = global_config.get("sudden_fall_prev_ar_min", 1.35)
        cur_ar_max = global_config.get("sudden_fall_cur_ar_max", 0.65)
        min_ar_drop = global_config.get("sudden_fall_min_drop", 0.7)
        min_person_bbox_area = global_config.get("min_person_bbox_area", 12000)
        min_confidence = global_config.get("fall_min_confidence", 0.5)

        incidents: List[Dict] = []
        for x1, y1, x2, y2, conf, tid in persons:
            bbox = (x1, y1, x2, y2)
            if conf < min_confidence or GeometryUtils.get_bbox_area(bbox) < min_person_bbox_area:
                continue
            ar = GeometryUtils.get_bbox_aspect_ratio(bbox)
            prev_ar, cur_ar = self.state_tracker.update_aspect_ratio(tid, ar)
            if prev_ar is not None:
                ar_drop = prev_ar - cur_ar
                if prev_ar > prev_ar_min and cur_ar < cur_ar_max and ar_drop > min_ar_drop:
                    incidents.append(self._incident(
                        "SUDDEN_FALL", camera_id, conf, bbox, tid,
                        f"Sudden fall — AR dropped from {prev_ar:.2f} to {cur_ar:.2f}",
                        "CRITICAL", aspect_ratio=cur_ar, ar_drop=ar_drop,
                    ))
        return incidents

    def _check_person_vehicle_impact(self, persons: List, vehicles: List,
                                     camera_id: str, cfg: Dict) -> List[Dict]:
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
                        pbox, pid,
                        f"Person-vehicle collision (IoU: {iou:.2f}, {dur / 5:.1f}s)",
                        "CRITICAL", iou=iou, vehicle_bbox=vbox,
                    ))
        return incidents

    def _check_vehicle_collision(self, vehicles: List, camera_id: str,
                                 cfg: Dict) -> List[Dict]:
        global_config = self.config.get("detection", {})
        required_frames = global_config.get("collision_detection_frames", 2)
        iou_threshold = global_config.get("collision_iou_threshold", 0.05)
        distance_threshold = global_config.get("collision_distance_threshold", 100)

        incidents: List[Dict] = []
        for i, (ax1, ay1, ax2, ay2, aconf, aid) in enumerate(vehicles):
            abox = (ax1, ay1, ax2, ay2)
            for bx1, by1, bx2, by2, bconf, bid in vehicles[i + 1:]:
                bbox_b = (bx1, by1, bx2, by2)
                iou = GeometryUtils.bbox_iou(abox, bbox_b)
                ac = GeometryUtils.get_centroid(abox)
                bc = GeometryUtils.get_centroid(bbox_b)
                dist = GeometryUtils.distance_between_points(ac, bc)
                colliding = iou > iou_threshold or dist < distance_threshold
                dur = self.state_tracker.update_collision_state(aid, colliding)
                if colliding and dur >= required_frames:
                    incidents.append(self._incident(
                        "VEHICLE_COLLISION", camera_id, min(aconf, bconf),
                        abox, aid,
                        f"Vehicle collision (IoU: {iou:.2f}, dist: {dist:.0f}px, {dur / 5:.1f}s)",
                        "CRITICAL", iou=iou, distance=dist,
                        vehicle_b_bbox=bbox_b,
                    ))
        return incidents

    def _check_ppe(self, persons: List, camera_id: str, cfg: Dict) -> List[Dict]:
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

    def _check_blast(self, frame: np.ndarray, camera_id: str) -> List[Dict]:
        global_config = self.config.get("detection", {})
        brightness_threshold = global_config.get("blast_brightness_threshold", 60)
        area_threshold = global_config.get("blast_area_threshold", 0.15)

        incidents: List[Dict] = []

        try:
            if len(frame.shape) == 3:
                gray = np.mean(frame, axis=2)
            else:
                gray = frame

            current_brightness = float(np.mean(gray))

            if self.prev_frame_brightness is not None:
                brightness_delta = current_brightness - self.prev_frame_brightness

                if brightness_delta > brightness_threshold:
                    bright_pixels = np.sum(gray > 200)
                    bright_percentage = bright_pixels / gray.size

                    if bright_percentage > area_threshold:
                        incidents.append(self._incident(
                            "BLAST_DETECTED", camera_id, 0.95,
                            (0, 0, frame.shape[1], frame.shape[0]), -1,
                            f"Explosion detected (brightness: {brightness_delta:.1f}, area: {bright_percentage * 100:.1f}%)",
                            "CRITICAL",
                            brightness_delta=brightness_delta,
                            bright_area_pct=bright_percentage,
                        ))

            self.prev_frame_brightness = current_brightness

        except Exception as e:
            logger.warning("Blast detection error: %s", e)

        return incidents

    def _check_fire(self, frame: np.ndarray, camera_id: str) -> List[Dict]:
        global_config = self.config.get("detection", {})
        fire_area_threshold = global_config.get("fire_area_threshold", 0.02)

        incidents: List[Dict] = []

        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([15, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])
            lower_orange = np.array([15, 100, 100])
            upper_orange = np.array([35, 255, 255])

            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

            fire_mask = mask_red1 | mask_red2 | mask_orange

            fire_pixels = np.sum(fire_mask > 0)
            fire_percentage = fire_pixels / fire_mask.size

            if fire_percentage > fire_area_threshold:
                contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    largest = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(largest)
                    bbox = (x, y, x + w, y + h)
                else:
                    bbox = (0, 0, frame.shape[1], frame.shape[0])

                incidents.append(self._incident(
                    "FIRE_DETECTED", camera_id, 0.90,
                    bbox, -1,
                    f"Fire detected (coverage: {fire_percentage * 100:.1f}%)",
                    "CRITICAL",
                    fire_area_pct=fire_percentage,
                ))

        except Exception as e:
            logger.warning("Fire detection error: %s", e)

        return incidents

    @staticmethod
    def _incident(type_: str, camera_id: str, confidence: float,
                  bbox: tuple, track_id: int, details: str,
                  severity: str, **extra) -> Dict:
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
