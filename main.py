#  Copyright (c) Made by Zhenyok!

import random
import time
from ctypes import windll

import cv2
import numpy as np
import pyautogui
import win32api
import win32con
from numpy.compat import unicode


def capture_screen():
    # Capture the screen
    screenshot = pyautogui.screenshot()
    # Convert the screenshot to a NumPy array
    frame = np.array(screenshot)
    # Convert the color format from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


def find_template(template, image):
    # Perform template matching
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.69  # Adjust the threshold to match your requirements
    loc = np.where(result >= threshold)
    # Get the center coordinates of all matches
    centers = []
    h, w = template.shape[:2]
    for pt in zip(*loc[::-1]):
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        centers.append((center_x, center_y))
    return centers


def char2key(c):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646329(v=vs.85).aspx
    result = windll.User32.VkKeyScanW(ord(unicode(c)))
    shift_state = (result & 0xFF00) >> 8
    vk_key = result & 0xFF

    return vk_key


def makeMove():
    move('s')
    time.sleep(0.8)
    stop('s')

    move('w')
    time.sleep(0.6)
    stop('w')

    time.sleep(0.5)

    move('e')
    time.sleep(1.7)
    stop('e')


def move(c):
    win32api.keybd_event(char2key(c), win32api.MapVirtualKey(char2key(c), 0), 0, 0)


def stop(c):
    win32api.keybd_event(char2key(c), win32api.MapVirtualKey(char2key(c), 0), win32con.KEYEVENTF_KEYUP, 0)


def main_loop(template_paths):
    # Load the template images
    templates = []
    for path in template_paths:
        template = cv2.imread(path, cv2.IMREAD_COLOR)
        # Convert the color format from BGR to RGB
        template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
        templates.append(template)

    while True:
        makeMove()
        for i in range(0, 11):
            frame = capture_screen()
            # send key down event
            for template in templates:
                centers = find_template(template, frame)
                # ssssweese
                if centers:
                    # Click on the center of the first match
                    center = list(centers[0])
                    for i in range(1, 6):
                        pyautogui.click(center[0], center[1])
                        time.sleep(i * random.uniform(0.15, 0.15))
                        center[0] += random.randint(-3, 3)
                        center[1] += random.randint(-3, 3)

                    break  # Move on to the next template image


if __name__ == '__main__':
    template_paths = [
        'boba2.jpeg']
    main_loop(template_paths)
