#  Copyright (c) Made by Zhenyok!

import time
from typing import Optional

import cv2 as cv2
import numpy as np
import pyautogui

from keyboard import Keyboard
from state import State

SUCCESS_TEMPLATE = cv2.cvtColor(cv2.imread('success.png'), cv2.COLOR_BGR2RGB)
FAILURE_TEMPLATE = cv2.cvtColor(cv2.imread('failure.png'), cv2.COLOR_BGR2RGB)


def biggest_component_y(binarized: np.ndarray) -> Optional[float]:
    analysis = cv2.connectedComponentsWithStats(binarized,
                                                4,
                                                cv2.CV_32S)
    (totalLabels, label_ids, values, centroid) = analysis
    if totalLabels > 1:
        # MAKING AVERAGE INDEXES
        index = np.argmax(values[1:, cv2.CC_STAT_AREA]) + 1
        mask = label_ids == index
        y_mask = np.sum(mask, axis=1)
        nonzeros = np.nonzero(y_mask)[0]
        rect_y = (nonzeros[0] + nonzeros[-1]) / 2
        return rect_y

    return None


def detect_fish(roi: np.ndarray) -> Optional[float]:
    roi_blue = roi[:, :, 2]
    ret, threshold = cv2.threshold(roi_blue, 215, 255, cv2.THRESH_BINARY_INV)
    return biggest_component_y(threshold)


def detect_rectangle(roi: np.ndarray) -> Optional[float]:
    roi_red = roi[:, :, 0]
    ret, threshold = cv2.threshold(roi_red, 175, 255, cv2.THRESH_BINARY)
    return biggest_component_y(threshold)


def cut_roi(frame: np.ndarray) -> np.ndarray:
    x_start, y_start = 965, 635
    x_end, y_end = 995, 919
    return frame[y_start:y_end, x_start:x_end]


def capture_screen() -> np.ndarray:
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


def capture_roi() -> np.ndarray:
    return cut_roi(capture_screen())


def is_fish_going_up() -> bool:
    roi = capture_roi()
    fish_y = detect_fish(roi)
    roi = capture_roi()
    fish_y2 = detect_fish(roi)
    return fish_y2 - fish_y < 0


def initialize_state() -> State:
    roi = capture_roi()
    rect_y = detect_rectangle(roi) or 141.5
    fish_y = detect_fish(roi) or 320

    return State(time.time(), fish_y=fish_y, rect_y=rect_y, fish_speed=0, rect_speed=0)


def find_template(template, image):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.80
    loc = np.where(result >= threshold)
    centers = []
    h, w = template.shape[:2]
    for pt in zip(*loc[::-1]):
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        centers.append((center_x, center_y))

    return image, centers


def detect_finished(screen: np.ndarray):
    for template in [SUCCESS_TEMPLATE, FAILURE_TEMPLATE]:
        image, centers = find_template(template, screen)
        if len(centers) > 0:
            # cv2.imshow("boba", image)
            # cv2.waitKey(0)
            return True
    return False


def start_fishing():
    Keyboard.press('e')
    time.sleep(0.7)
    Keyboard.release('e')
    time.sleep(0.7)
    Keyboard.press_left_click()
    time.sleep(0.7)
    Keyboard.press_left_click()


def fishing_process():
    start_time = time.time()
    state = initialize_state()

    i = 0
    while True:
        i = (i + 1) % 23
        screen = capture_screen()
        roi = cut_roi(screen)

        rect_y = detect_rectangle(roi)
        fish_y = detect_fish(roi)
        if i == 0 and np.isclose(fish_y, 141.5) and detect_finished(screen):
            break

        if np.isclose(fish_y, 141.5):
            Keyboard.release(' ')
            continue

        if rect_y is None:
            rect_y = 320

        elapsed_time = time.time() - start_time
        state = State.from_previous_state(state, elapsed_time, fish_y, rect_y)

        delta = (state.rect_speed - state.fish_speed) ** 2 \
                - 4 * state.FREE_FALL_ACCELERATION * (state.rect_y - state.fish_y)

        if state.rect_speed > 40 and state.fish_speed < 0:
            Keyboard.press(' ')
            time.sleep(0.15)
            Keyboard.release(' ')
        elif state.rect_speed - state.fish_speed > 70:
            Keyboard.press(' ')
            time.sleep(0.15)
            Keyboard.release(' ')

        if delta < 50:
            Keyboard.press(' ')
            time.sleep(0.1)
            Keyboard.release(' ')


def main():
    while True:
        start_fishing()
        time.sleep(4.0)
        fishing_process()
        time.sleep(1.0)


if __name__ == '__main__':
    template_paths = [
        'failure.png', 'success.png']
    main()
