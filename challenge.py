import time
import logging
import numpy as np
import cv2
import pyautogui
from dataclasses import dataclass
from utils import capture_screen_cropped, logger

CONFIDENCE_THRESHOLD = 0.8
DUPLICATE_DISTANCE = 30
FAIL_FAST_TIMEOUT = 3.0
REQUIRED_ARROW_COUNT = 7

@dataclass
class ArrowMatch:
    x: int
    y: int
    direction: str
    confidence: float
    w: int
    h: int

def parse_arrows_with_templates(current_shot: np.ndarray, templates: dict[str, np.ndarray]) -> list[str] | None:
    found_arrows: list[ArrowMatch] = []

    for direction, tmpl in templates.items():
        h, w = tmpl.shape
        res = cv2.matchTemplate(current_shot, tmpl, cv2.TM_CCOEFF_NORMED)
        y_locs, x_locs = np.where(res >= CONFIDENCE_THRESHOLD)

        for x, y in zip(x_locs, y_locs):
            confidence = float(res[y, x])
            new_match = ArrowMatch(int(x), int(y), direction, confidence, w, h)

            is_new = True
            for existing in found_arrows:
                if abs(new_match.x - existing.x) < DUPLICATE_DISTANCE and abs(new_match.y - existing.y) < DUPLICATE_DISTANCE:
                    is_new = False
                    if new_match.confidence > existing.confidence:
                        existing.confidence = new_match.confidence
                        existing.direction = new_match.direction
                        existing.w = new_match.w
                        existing.h = new_match.h
                    break
            if is_new:
                found_arrows.append(new_match)

    if len(found_arrows) != REQUIRED_ARROW_COUNT:
        return None

    found_arrows.sort(key=lambda m: m.x)
    return [m.direction for m in found_arrows]

def play(
    bbox: tuple[int, int, int, int],
    scale_x: float,
    scale_y: float,
    templates: dict[str, np.ndarray],
    rounds_to_play: int = 3,
    key_delay: float = 0.05,
    round_delay: float = 0.3
) -> int:
    logger.info("--- Starting Challenge Minigame ---")
    rounds_completed = 0
    wait_start_time = time.time()

    while rounds_completed < rounds_to_play:
        current_shot = capture_screen_cropped(bbox)
        directions = parse_arrows_with_templates(current_shot, templates)

        if directions:
            logger.info(f"[Challenge] Round {rounds_completed + 1}: {directions}")
            for direction in directions:
                pyautogui.press(direction)
                time.sleep(key_delay)

            rounds_completed += 1
            wait_start_time = time.time()

            if rounds_completed < rounds_to_play:
                time.sleep(round_delay)
        else:
            if time.time() - wait_start_time > FAIL_FAST_TIMEOUT:
                logger.warning("[Challenge] No arrows detected. Minigame likely ended or didn't start.")
                break
        time.sleep(0.05)

    logger.info("--- Exiting Challenge Minigame ---")
    return rounds_completed