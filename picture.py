import time

import cv2 as cv2
import numpy as np
import pyautogui

from main import move, stop


def boba_fish(frame):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    x_start, y_start = 965, 635
    x_end, y_end = 995, 919
    roi = img_gray[y_start:y_end, x_start:x_end]

    # DETECTING FISHHH!!!!!!!!!!!!!!!!!!!!!!
    roi_blue = roi[:, :, 2]

    ret, threshold = cv2.threshold(roi_blue, 220, 255, cv2.THRESH_BINARY_INV)

    analysis = cv2.connectedComponentsWithStats(threshold,
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


def boba_rect(frame):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    x_start, y_start = 965, 635
    x_end, y_end = 995, 980
    roi = img_gray[y_start:y_end, x_start:x_end]

    # DETECTING RECTANGLE!!!!!!!!!!!!!!!!!!!!!!!!!
    roi_red = roi[:, :, 0]

    ret, threshold = cv2.threshold(roi_red, 175, 255, cv2.THRESH_BINARY)

    analysis = cv2.connectedComponentsWithStats(threshold,
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

    return boba_rect(capture_screen())


def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


def going_up():
    frame = capture_screen()
    fish_y = boba_fish(frame)
    frame = capture_screen()
    fish_y2 = boba_fish(frame)
    return fish_y2 - fish_y < 0


# start_time = time.time()
# elapsed_time = time.time() - start_time
# formatted_time = "{:.3f}".format(elapsed_time)
# print("rect = ", rect_y, " fish = ", fish_y, f"Time: {formatted_time}")


def second_boba():
    start_time = time.time()
    while True:
        frame = capture_screen()
        rect_y = boba_rect(frame)
        fish_y = boba_fish(frame)
        elapsed_time = time.time() - start_time
        formatted_time = "{:.3f}".format(elapsed_time)
        print("rect = ", rect_y, " fish = ", fish_y, f"Time: {formatted_time}")

        # while abs(rect_y - fish_y) > 30:
        #     move(' ')
        #     time.sleep(0.08)
        #     stop(' ')
        #     time.sleep(0.02)
        #     frame = capture_screen()
        #     rect_y = boba_rect(frame)
        #     fish_y = boba_fish(frame)
        #
        # while abs(rect_y - fish_y) < 30:
        #     while going_up():
        #         move(' ')
        #         time.sleep(0.11)
        #         stop(' ')
        #         time.sleep(0.06)
        #         frame = capture_screen()
        #         rect_y = boba_rect(frame)
        #         fish_y = boba_fish(frame)
        #         print('up')
        #     while not going_up():
        #         move(' ')
        #         time.sleep(0.11)
        #         stop(' ')
        #         time.sleep(0.08)
        #         frame = capture_screen()
        #         rect_y = boba_rect(frame)
        #         fish_y = boba_fish(frame)
        #         print('down')

        # if rect_y is not None and abs(rect_y - fish_y) < 5:
        #     while going_up():
        #         move(' ')
        #         time.sleep(0.075)
        #         stop(' ')
        #         time.sleep(0.02)
        #
        #     while not going_up():
        #         move(' ')
        #         time.sleep(0.06)
        #         stop(' ')
        #         time.sleep(0.02)

        #     if not going_up():
        #         while rect_y < fish_y:
        #             frame = capture_screen()
        #             fish_y = boba_fish(frame)
        #             rect_y = boba_rect(frame)
        #             move(' ')
        #         stop(' ')


if __name__ == '__main__':
    template_paths = [
        'boba2.jpeg']
    second_boba()
