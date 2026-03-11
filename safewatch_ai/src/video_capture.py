import logging
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class VideoCapture:

    def __init__(self, source: str):
        self.source = source
        self.cap: Optional[cv2.VideoCapture] = None
        self.fps = 30.0
        self.frame_width = 0
        self.frame_height = 0
        self.total_frames = 0
        self.current_frame_idx = 0
        self._open()

    def _open(self) -> None:
        try:
            src = int(self.source)
        except (ValueError, TypeError):
            src = self.source

        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video source: {self.source}")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        logger.info("Video opened: %dx%d @ %.1f FPS",
                     self.frame_width, self.frame_height, self.fps)

    def release(self) -> None:
        if self.cap:
            self.cap.release()

    def __del__(self) -> None:
        self.release()

    def get_frame(self) -> Optional[np.ndarray]:
        if self.cap is None:
            return None
        ok, frame = self.cap.read()
        if ok:
            self.current_frame_idx += 1
            return frame
        return None

    def get_fps(self) -> float:
        return self.fps

    def get_resolution(self) -> tuple[int, int]:
        return (self.frame_width, self.frame_height)

    def get_frame_count(self) -> int:
        return self.total_frames or 0
