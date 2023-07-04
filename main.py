import pyautogui
import cv2
import numpy as np
import time
import random


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


def main_loop(template_paths):
    # Load the template images
    templates = []
    for path in template_paths:
        template = cv2.imread(path, cv2.IMREAD_COLOR)
        # Convert the color format from BGR to RGB
        template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
        templates.append(template)

    while True:
        # Capture the screen
        frame = capture_screen()
        # Find the center coordinates of all template images
        for template in templates:
            centers = find_template(template, frame)
            if centers:
                # Click on the center of the first match
                center = list(centers[0])
                for i in range(1, 6):
                    pyautogui.click(center[0], center[1])
                    time.sleep(i*random.uniform(0.15, 0.2))
                    center[0] += random.randint(-3, 3)
                    center[1] += random.randint(-3, 3)

                time.sleep(random.uniform(0.4, 1))  # Optional delay between clicks
                break  # Move on to the next template image


if __name__ == '__main__':
    template_paths = [
        'C:/Users/Zhenya/Downloads/boba2.jpeg']
    main_loop(template_paths)
