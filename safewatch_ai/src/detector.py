"""Ultralytics YOLO-based detector for industrial safety monitoring."""

import logging
from typing import Dict, List

import cv2
import numpy as np
from ultralytics import YOLO

logger = logging.getLogger(__name__)

# COCO classes that matter for safety monitoring
_VEHICLE_CLASSES = {"car", "truck", "bus", "motorbike"}


class SafetyDetector:
    """Detect persons and vehicles in video frames using Ultralytics YOLO."""
    
    def __init__(self, model_name: str = "yolo26n.pt",
                 confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold
        self.object_tracks: Dict[int, tuple] = {}   # track_id → (class, centroid)
        self.next_track_id = 1

        logger.info("Loading YOLO model: %s", model_name)
        self.model = YOLO(model_name)
        logger.info("Model loaded")
    
    def detect(self, frame: np.ndarray) -> Dict:
        """Run inference and return ``{persons, vehicles, ppe}``.

        Each person / vehicle entry is ``[x1, y1, x2, y2, conf, track_id]``.
        """
        empty: Dict = {"persons": [], "vehicles": [], "ppe": {"hardhat": [], "vest": []}}

        try:
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
        except Exception as e:
            logger.error("Detection error: %s", e)
            return empty

        if not results or results[0].boxes is None:
            return empty

        detections: Dict = {"persons": [], "vehicles": [], "ppe": {"hardhat": [], "vest": []}}
        names = self.model.names  # built-in id → name mapping

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0])
            cls_name = names.get(int(box.cls[0]), "unknown")
            track_id = self._get_track_id(x1, y1, x2, y2, cls_name)
            entry = [x1, y1, x2, y2, conf, track_id]

            if cls_name == "person":
                detections["persons"].append(entry)
            elif cls_name in _VEHICLE_CLASSES:
                detections["vehicles"].append(entry)

        return detections
    
    def _get_track_id(self, x1: int, y1: int, x2: int, y2: int,
                       class_name: str) -> int:
        """Simple centroid-based tracker — match or create a new ID."""
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        best_dist, best_id = float("inf"), None

        for tid, (prev_cls, prev_c) in list(self.object_tracks.items()):
            if prev_cls != class_name:
                continue
            d = np.hypot(cx - prev_c[0], cy - prev_c[1])
            if d < best_dist and d < 100:
                best_dist, best_id = d, tid

        if best_id is not None:
            self.object_tracks[best_id] = (class_name, (cx, cy))
            return best_id

        new_id = self.next_track_id
        self.next_track_id += 1
        self.object_tracks[new_id] = (class_name, (cx, cy))
        return new_id
    
    def draw_detections(self, frame: np.ndarray, detections: Dict,
                       with_ids: bool = True,
                       with_classes: bool = True) -> np.ndarray:
        """Annotate *frame* with bounding boxes and labels."""
        out = frame.copy()

        for category, colour, label_base in [
            ("persons",  (0, 255, 0), "Person"),
            ("vehicles", (0, 0, 255), "Vehicle"),
        ]:
            for x1, y1, x2, y2, conf, tid in detections.get(category, []):
                cv2.rectangle(out, (x1, y1), (x2, y2), colour, 2)
                parts = [label_base] if with_classes else []
                if with_ids:
                    parts.append(f"#{tid}")
                parts.append(f"{conf:.2f}")
                cv2.putText(out, " ".join(parts), (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)

        return out
