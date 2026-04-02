from __future__ import annotations

import logging
import numpy as np
from PIL import ImageGrab

logger = logging.getLogger(__name__)

def capture_screen_cropped(bbox: tuple[int, int, int, int] | None = None) -> np.ndarray:
    """Captures the screen in grayscale. Optionally crops to (x1, y1, x2, y2)."""
    screen = ImageGrab.grab().convert('L')
    img = np.array(screen)
    if bbox:
        x1, y1, x2, y2 = bbox
        return img[y1:y2, x1:x2]
    return img