"""Object and state trackers used by the rule engine."""

import logging
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)


# ────────────────────────────────────────────────────────────────────
# Centroid-based object tracker (standalone, used by tests)
# ────────────────────────────────────────────────────────────────────

class ObjectTracker:
    """Match detections across frames via centroid proximity."""

    def __init__(self, max_distance: float = 100.0, max_age: int = 30):
        self.max_distance = max_distance
        self.max_age = max_age
        self.tracks: Dict[int, dict] = {}
        self.next_track_id = 1
        self.frame_count = 0

    def update(self, detections: List[Dict],
               frame_idx: Optional[int] = None) -> Dict:
        """Match *detections* (each must have ``bbox``) to existing tracks."""
        self.frame_count = frame_idx if frame_idx is not None else self.frame_count + 1

        # Current centroids
        cur = {}
        for i, det in enumerate(detections):
            bbox = det.get("bbox")
            if bbox:
                x1, y1, x2, y2 = bbox
                cur[i] = {"point": ((x1 + x2) // 2, (y1 + y2) // 2), "det": det}

        matched, used = {}, set()

        # Greedy nearest-neighbour matching
        for tid, info in list(self.tracks.items()):
            prev = info["centroid"]
            best_d, best_i = float("inf"), None
            for i, c in cur.items():
                if i in used:
                    continue
                d = np.hypot(prev[0] - c["point"][0], prev[1] - c["point"][1])
                if d < self.max_distance and d < best_d:
                    best_d, best_i = d, i
            if best_i is not None:
                info["centroid"] = cur[best_i]["point"]
                info["age"] = 0
                info["detection"] = cur[best_i]["det"]
                used.add(best_i)
                matched[tid] = info

        # New tracks for unmatched detections
        for i, c in cur.items():
            if i not in used:
                tid = self.next_track_id
                self.next_track_id += 1
                self.tracks[tid] = {
                    "centroid": c["point"], "age": 0,
                    "detection": c["det"], "created_at": self.frame_count,
                }
                matched[tid] = self.tracks[tid]

        # Age-out stale tracks
        for tid in list(self.tracks):
            if tid not in matched:
                self.tracks[tid]["age"] += 1
                if self.tracks[tid]["age"] > self.max_age:
                    del self.tracks[tid]

        return {tid: t["detection"] for tid, t in matched.items()}

    def get_tracks(self) -> Dict:
        return dict(self.tracks)

    def reset(self) -> None:
        self.tracks.clear()
        self.next_track_id = 1
        self.frame_count = 0


# ────────────────────────────────────────────────────────────────────
# Per-object state tracker (used by RuleEngine)
# ────────────────────────────────────────────────────────────────────

class StateTracker:
    """Accumulate per-object state (fall frames, proximity, zones, motion)."""

    _DEFAULT_STATE = {
        "fall_frames": 0,
        "proximity_frames": 0,
        "zone_entry_frame": None,
        "last_position": None,
        "motionless_frames": 0,
        "prev_aspect_ratio": None,
        "collision_frames": 0,
        "impact_frames": 0,
    }

    def __init__(self):
        self._states: Dict[int, dict] = defaultdict(
            lambda: dict(self._DEFAULT_STATE)
        )

    # ── fall ────────────────────────────────────────────────────────

    def update_fall_state(self, tid: int, is_falling: bool) -> None:
        s = self._states[tid]
        s["fall_frames"] = s["fall_frames"] + 1 if is_falling else 0

    def get_fall_duration(self, tid: int) -> int:
        return self._states[tid]["fall_frames"]

    # ── proximity ───────────────────────────────────────────────────

    def update_proximity_state(self, tid: int, in_prox: bool) -> int:
        s = self._states[tid]
        s["proximity_frames"] = s["proximity_frames"] + 1 if in_prox else 0
        return s["proximity_frames"]

    # ── zone entry ──────────────────────────────────────────────────

    def update_zone_entry(self, tid: int, in_zone: bool, frame: int) -> None:
        s = self._states[tid]
        if in_zone:
            if s["zone_entry_frame"] is None:
                s["zone_entry_frame"] = frame
        else:
            s["zone_entry_frame"] = None

    def get_zone_entry_frame(self, tid: int) -> Optional[int]:
        return self._states[tid]["zone_entry_frame"]

    # ── motionless ──────────────────────────────────────────────────

    def update_motionless_state(self, tid: int, pos: Tuple[float, float],
                                threshold: float = 15) -> int:
        """Increment motionless counter if movement < *threshold* px."""
        s = self._states[tid]
        prev = s["last_position"]
        if prev is not None:
            d = np.hypot(pos[0] - prev[0], pos[1] - prev[1])
            s["motionless_frames"] = s["motionless_frames"] + 1 if d < threshold else 0
        s["last_position"] = pos
        return s["motionless_frames"]

    # ── sudden fall (AR change) ─────────────────────────────────────

    def update_aspect_ratio(self, tid: int, ar: float) -> Tuple[Optional[float], float]:
        """Store current AR; return (prev_ar, current_ar)."""
        s = self._states[tid]
        prev = s["prev_aspect_ratio"]
        s["prev_aspect_ratio"] = ar
        return prev, ar

    # ── vehicle collision ───────────────────────────────────────────

    def update_collision_state(self, vid: int, colliding: bool) -> int:
        s = self._states[vid]
        s["collision_frames"] = s["collision_frames"] + 1 if colliding else 0
        return s["collision_frames"]

    # ── person-vehicle impact ───────────────────────────────────────

    def update_impact_state(self, pid: int, impacting: bool) -> int:
        s = self._states[pid]
        s["impact_frames"] = s["impact_frames"] + 1 if impacting else 0
        return s["impact_frames"]

    # ── cleanup ─────────────────────────────────────────────────────

    def reset_track(self, tid: int) -> None:
        self._states.pop(tid, None)
