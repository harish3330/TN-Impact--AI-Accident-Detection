"""Geometry helpers for bounding-box math and polygon operations."""

from typing import List, Tuple

import cv2
import numpy as np


class GeometryUtils:
    """Pure static utility class – no state, no side-effects."""

    # ── point-in-polygon ────────────────────────────────────────────

    @staticmethod
    def point_in_polygon(point: Tuple[float, float],
                         polygon: List[Tuple[float, float]]) -> bool:
        """Ray-casting algorithm. Returns ``True`` when *point* is inside."""
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    # ── bounding-box helpers ────────────────────────────────────────

    @staticmethod
    def get_centroid(bbox: Tuple[int, int, int, int]) -> Tuple[int, int]:
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    @staticmethod
    def get_bbox_area(bbox: Tuple[int, int, int, int]) -> int:
        x1, y1, x2, y2 = bbox
        return (x2 - x1) * (y2 - y1)

    @staticmethod
    def get_bbox_aspect_ratio(bbox: Tuple[int, int, int, int]) -> float:
        """Return *height / width* (> 1 → standing, < 0.7 → lying)."""
        x1, y1, x2, y2 = bbox
        return max(1, y2 - y1) / max(1, x2 - x1)

    @staticmethod
    def get_bbox_angle(bbox: Tuple[int, int, int, int]) -> float:
        """Simplified angle: 0° standing, 90° lying."""
        x1, y1, x2, y2 = bbox
        return 90.0 if (x2 - x1) > (y2 - y1) else 0.0

    # ── distance helpers ────────────────────────────────────────────

    @staticmethod
    def distance_between_points(p1: Tuple[float, float],
                                p2: Tuple[float, float]) -> float:
        return float(np.hypot(p1[0] - p2[0], p1[1] - p2[1]))

    @staticmethod
    def distance_point_to_bbox(point: Tuple[float, float],
                               bbox: Tuple[int, int, int, int]) -> float:
        """Minimum Euclidean distance from *point* to the bbox boundary."""
        x, y = point
        x1, y1, x2, y2 = bbox
        cx = max(x1, min(x, x2))
        cy = max(y1, min(y, y2))
        return float(np.hypot(x - cx, y - cy))

    @staticmethod
    def bbox_iou(a: Tuple[int, int, int, int],
                 b: Tuple[int, int, int, int]) -> float:
        """Intersection-over-Union of two bounding boxes."""
        ix1 = max(a[0], b[0])
        iy1 = max(a[1], b[1])
        ix2 = min(a[2], b[2])
        iy2 = min(a[3], b[3])
        if ix2 < ix1 or iy2 < iy1:
            return 0.0
        inter = (ix2 - ix1) * (iy2 - iy1)
        union = ((a[2] - a[0]) * (a[3] - a[1]) +
                 (b[2] - b[0]) * (b[3] - b[1]) - inter)
        return inter / union if union else 0.0

    # ── drawing ─────────────────────────────────────────────────────

    @staticmethod
    def draw_polygon(frame: np.ndarray,
                     polygon: List[Tuple[int, int]],
                     color: Tuple[int, int, int] = (0, 255, 0),
                     thickness: int = 2,
                     label: str = "") -> np.ndarray:
        """Draw a closed polygon (and optional label) on a copy of *frame*."""
        out = frame.copy()
        if len(polygon) < 2:
            return out
        pts = np.array(polygon, dtype=np.int32)
        cv2.polylines(out, [pts], True, color, thickness)
        if label:
            cv2.putText(out, label, polygon[0],
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return out
