import os
import time
import logging
import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab
from typing import Sequence
from utils import capture_screen_cropped, logger
import fight
import challenge

# Configuration
SETUP_DELAY = 3
TEMPLATES_DIRECTORY = "templates"
CHECK_INTERVAL = 30
FIGHT_COOLDOWN = 180
CHALLENGE_COOLDOWN = 120

pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

def load_templates() -> dict[str, np.ndarray] | None:
    templates = {}
    directions = ["up", "down", "left", "right"]
    for direction in directions:
        filepath = os.path.join(TEMPLATES_DIRECTORY, f"template_{direction}.png")
        if not os.path.exists(filepath):
            logger.critical(f"Could not find template file: '{filepath}'")
            return None
        templates[direction] = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    logger.info("All arrow templates loaded successfully.")
    return templates

def setup_working_area() -> tuple[tuple[int, int, int, int], list[tuple[float, float]]] | None:
    logger.info("Taking screenshot for ROI selection...")
    screen_gray = capture_screen_cropped()
    screen_bgr = cv2.cvtColor(screen_gray, cv2.COLOR_GRAY2BGR)

    window_name = "Setup: 1. Select ROI | 2. Pinpoint Buttons"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    try:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    except Exception:
        logger.warning("Fullscreen window property not supported on this platform. Continuing normally.")

    instruction_img = screen_bgr.copy()
    cv2.putText(instruction_img, "STEP 1: Draw a box over the GAME WINDOW and press ENTER",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    logger.info("\n--- STEP 1 ---\nDraw a box over your ENTIRE GAME WINDOW and press ENTER.")
    roi = cv2.selectROI(window_name, instruction_img, showCrosshair=True, fromCenter=False)
    x, y, w, h = map(int, roi)

    if w == 0 or h == 0:
        logger.warning("ROI selection cancelled (width/height is 0).")
        cv2.destroyWindow(window_name)
        return None

    roi_crop = screen_bgr[y:y+h, x:x+w]
    button_coords: list[tuple[float, float]] = []
    btn_labels = ["ADVENTURE", "CHALLENGE", "FIGHT", "CONTINUE"]

    def mouse_callback(event: int, mx: int, my: int, flags: int, param: None) -> None:
        if event == cv2.EVENT_LBUTTONDOWN and len(button_coords) < 4:
            button_coords.append((mx / w, my / h))
            logger.info(f"Set {btn_labels[len(button_coords)-1]} position.")

    cv2.setMouseCallback(window_name, mouse_callback)
    logger.info("\n--- STEP 2 ---\nClick the buttons in order: Adventure -> Challenge -> Fight -> Continue")

    while len(button_coords) < 4:
        display_img = roi_crop.copy()
        current_label = btn_labels[len(button_coords)]

        cv2.rectangle(display_img, (5, 5), (450, 45), (0, 0, 0), -1)
        cv2.putText(display_img, f"STEP 2: Click the {current_label} button",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow(window_name, display_img)
        if cv2.waitKey(1) & 0xFF == 27:
            logger.warning("Setup aborted by user.")
            break

    cv2.destroyWindow(window_name)
    cv2.waitKey(1)

    if len(button_coords) < 4:
        return None

    bbox = (x, y, x + w, y + h)
    return bbox, button_coords

def click_relative(bbox: tuple[int, int, int, int], x_pct: float, y_pct: float, scale_x: float, scale_y: float) -> None:
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1

    target_x = int((x1 + (width * x_pct)) / scale_x)
    target_y = int((y1 + (height * y_pct)) / scale_y)

    pyautogui.moveTo(target_x, target_y)
    time.sleep(0.5)
    pyautogui.leftClick()

def did_screen_change(img_before: np.ndarray, img_after: np.ndarray, threshold: int = 20, min_pct_change: float = 0.25) -> bool:
    diff = cv2.absdiff(img_before, img_after)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    changed_pixels = cv2.countNonZero(thresh)
    total_pixels = img_before.shape[0] * img_before.shape[1]
    return (changed_pixels / total_pixels) > min_pct_change

def main() -> None:
    print("-" * 50)
    print("LAST MEADOW ONLINE AUTOMATION")
    print("NOTICE: This script is for educational use only.")
    print("The author is not responsible for account bans or misuse.")
    print("-" * 50)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
    
    templates = load_templates()
    if not templates:
        return

    logical_w, logical_h = pyautogui.size()
    phys_w, phys_h = ImageGrab.grab().size
    scale_x = phys_w / logical_w
    scale_y = phys_h / logical_h
    logger.info(f"Display scaling factors: X={scale_x:.2f}, Y={scale_y:.2f}")

    logger.info(f"You have {SETUP_DELAY} seconds to switch workspace...")
    time.sleep(SETUP_DELAY)

    setup_result = setup_working_area()
    if not setup_result:
        logger.error("Setup cancelled or failed.")
        return

    bbox, button_pcts = setup_result
    (btn_adv_x, btn_adv_y), (btn_chall_x, btn_chall_y), (btn_fight_x, btn_fight_y), (btn_cont_x, btn_cont_y) = button_pcts

    logger.info("\n--- STARTED ---")
    time.sleep(3)

    last_fight_time = 0.0
    last_challenge_time = 0.0
    last_priority_check = 0.0

    try:
        while True:
            current_time = time.time()

            if current_time - last_priority_check >= CHECK_INTERVAL:
                logger.info(f"\n{CHECK_INTERVAL}s elapsed. Performing Priority Check...")
                last_priority_check = current_time

                # Fight Check
                if current_time - last_fight_time >= FIGHT_COOLDOWN:
                    logger.info("Checking Fight...")
                    img_before = capture_screen_cropped(bbox)
                    click_relative(bbox, btn_fight_x, btn_fight_y, scale_x, scale_y)
                    time.sleep(1.0)
                    img_after = capture_screen_cropped(bbox)

                    if did_screen_change(img_before, img_after):
                        result = fight.play(bbox, scale_x, scale_y)
                        if result == 10:
                            last_fight_time = time.time()
                            click_relative(bbox, btn_cont_x, btn_cont_y, scale_x, scale_y)

                # Challenge Check
                if current_time - last_challenge_time >= CHALLENGE_COOLDOWN:
                    logger.info("Checking Challenge...")
                    img_before = capture_screen_cropped(bbox)
                    click_relative(bbox, btn_chall_x, btn_chall_y, scale_x, scale_y)
                    time.sleep(1.0)
                    img_after = capture_screen_cropped(bbox)

                    if did_screen_change(img_before, img_after):
                        result = challenge.play(bbox, scale_x, scale_y, templates)
                        if result == 3:
                            last_challenge_time = time.time()
                            click_relative(bbox, btn_cont_x, btn_cont_y, scale_x, scale_y)

            # Dungeon/Clicker Mode
            logger.debug("Entering Dungeon/Clicker mode...")
            click_relative(bbox, btn_adv_x, btn_adv_y, scale_x, scale_y)

            while time.time() - last_priority_check < CHECK_INTERVAL:
                pyautogui.leftClick()
                time.sleep(0.01)
                if np.random.rand() > 0.95:
                    time.sleep(0.05)

    except pyautogui.FailSafeException:
        logger.info("\nFail-safe triggered. Master Script stopped.")
    except KeyboardInterrupt:
        logger.info("\nScript manually terminated.")

if __name__ == "__main__":
    main()