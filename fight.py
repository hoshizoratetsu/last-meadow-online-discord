import time
import logging
import numpy as np
import cv2
import pyautogui
from utils import capture_screen_cropped, logger

THRESHOLD = 80
BRIGHT_THRESHOLD = 100
MIN_AREA = 150
MAX_AREA = 10000
CIRCULARITY_TOLERANCE = 0.7
FAIL_FAST_TIMEOUT = 7.0
CLICK_LIMIT = 10

def find_new_black_circles(baseline: np.ndarray, current: np.ndarray) -> list[tuple[int, int]]:
    was_bright = baseline > BRIGHT_THRESHOLD
    is_now_black = current < THRESHOLD
    new_black_mask = (was_bright & is_now_black).astype(np.uint8) * 255

    contours, _ = cv2.findContours(new_black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers: list[tuple[int, int]] = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < MIN_AREA or area > MAX_AREA:
            continue

        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue

        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if circularity >= CIRCULARITY_TOLERANCE:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))
    return centers

def move_to_target(cx: int, cy: int, offset_x: int, offset_y: int, scale_x: float, scale_y: float) -> None:
    target_x = int((offset_x + cx) / scale_x)
    target_y = int((offset_y + cy) / scale_y)
    logger.debug(f"[Fight] Moving to target: {target_x}, {target_y}")
    pyautogui.moveTo(target_x, target_y)

def play(
    bbox: tuple[int, int, int, int],
    scale_x: float,
    scale_y: float,
    click_limit: int = CLICK_LIMIT
) -> int:
    logger.info("--- Starting Fight Minigame ---")
    offset_x = bbox[0] if bbox else 0
    offset_y = bbox[1] if bbox else 0

    baseline = capture_screen_cropped(bbox)
    wait_start_time = time.time()
    clicks_done = 0

    while clicks_done < click_limit:
        current_shot = capture_screen_cropped(bbox)
        circle_centers = find_new_black_circles(baseline, current_shot)

        if circle_centers:
            cx, cy = circle_centers[0]
            move_to_target(cx, cy, offset_x, offset_y, scale_x, scale_y)
            
            time.sleep(0.05)
            pyautogui.leftClick()
            clicks_done += 1
            logger.info(f"[Fight] Progress: {clicks_done}/{click_limit}")

            baseline = current_shot
            wait_start_time = time.time()
            time.sleep(0.3)
        else:
            if time.time() - wait_start_time > FAIL_FAST_TIMEOUT:
                logger.warning("[Fight] No targets detected for too long. Exiting module.")
                break
        time.sleep(0.05)

    logger.info("--- Exiting Fight Minigame ---")
    return clicks_done