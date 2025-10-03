"""
GOAL: build a single organized screen showing the whole pipeline (progression of image processing steps)
create one blank canvas. (Big black image)
Paste each state image image into a fixed slot on that that canvas. (Top-Left,Top-Right, Bottom-Row, etc.)
Gives a dashbord view of the whole pipeline.
"""
# display.py
import cv2
import numpy as np
from typing import Dict, Tuple, Optional

# Type aliases
Point = Tuple[int, int]          # (x, y)
Size  = Tuple[int, int]          # (w, h)
Slot  = Tuple[Point, Size]       # ((x, y), (w, h))

def _to_bgr(img: Optional[np.ndarray]) -> np.ndarray:
    """Ensure an image is BGR with 3 channels; return black if None."""
    if img is None:
        return np.zeros((10, 10, 3), dtype=np.uint8)
    if img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.ndim == 3 and img.shape[2] == 3:
        return img
    return np.zeros((10, 10, 3), dtype=np.uint8)

def _fit_into(img: np.ndarray, size: Size, keep_aspect: bool = True) -> np.ndarray:
    """Resize img to fit into size (w,h); pad with black if keeping aspect."""
    w, h = size
    if not keep_aspect:
        return cv2.resize(img, (w, h))
    ih, iw = img.shape[:2]
    if iw == 0 or ih == 0:  # avoid div-by-zero
        return np.zeros((h, w, 3), dtype=np.uint8)

    scale = min(w / iw, h / ih)
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    resized = cv2.resize(img, (nw, nh))

    # pad to slot size (letterbox)
    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    x0 = (w - nw) // 2
    y0 = (h - nh) // 2
    canvas[y0:y0+nh, x0:x0+nw] = resized
    return canvas

class Dashboard:
    """
    One-window dashboard:
      - A big black canvas (e.g., your monitor resolution)
      - Fixed slots you define: slot_name -> ((x,y), (w,h))
      - Each update() pastes frames into their slots and shows once
    """

    def __init__(
        self,
        window_name: str,
        canvas_size: Size,                  # e.g., (1920, 1080)
        slots: Dict[str, Slot],             # {'main': ((0,0),(1280,720)), 'roi': ((1280,0),(640,360)), ...}
        fullscreen: bool = True,
        keep_aspect: bool = True,
        show_labels: bool = True
    ):
        self.window_name = window_name
        self.canvas_size = canvas_size
        self.slots = slots
        self.keep_aspect = keep_aspect
        self.show_labels = show_labels

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        if fullscreen:
            try:
                cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            except Exception:
                # Fallback: maximize window if fullscreen not supported
                cv2.resizeWindow(self.window_name, canvas_size[0], canvas_size[1])

    def update(self, frames: Dict[str, Optional[np.ndarray]]) -> None:
        """
        frames: dict mapping slot_name -> image (BGR or gray). Missing slots get black.
        """
        W, H = self.canvas_size
        canvas = np.zeros((H, W, 3), dtype=np.uint8)

        for name, ((x, y), (w, h)) in self.slots.items():
            img = _to_bgr(frames.get(name))
            img = _fit_into(img, (w, h), keep_aspect=self.keep_aspect)

            # Optional label
            if self.show_labels:
                cv2.putText(img, name, (10, 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

            # Paste into canvas, clamped to bounds
            x2, y2 = min(x + w, W), min(y + h, H)
            slot_w, slot_h = x2 - x, y2 - y
            if slot_w > 0 and slot_h > 0:
                roi = img[:slot_h, :slot_w]
                canvas[y:y2, x:x2] = roi

        cv2.imshow(self.window_name, canvas)
