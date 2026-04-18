import cv2
import numpy as np
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Vision:
    def __init__(self):

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        fish_path = os.path.join(base_path, "fish.png")

        fish_img = cv2.imread(fish_path, cv2.IMREAD_GRAYSCALE)

        if fish_img is None:
            raise RuntimeError(f"fish.png bulunamadı -> {fish_path}")

        self.fish_template = fish_img
        self.fw, self.fh = self.fish_template.shape[::-1]

        self.bar_x = 490
        self.bar_y = 214
        self.bar_w = 315
        self.bar_h = 20

        self.last_fish_x = None


    def get_bar(self, img):

        x, y, w, h = self.bar_x, self.bar_y, self.bar_w, self.bar_h
        roi = img[y:y+h, x:x+w]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_ratio = np.sum(blue_mask > 0) / (w * h)

        if blue_ratio < 0.5:
            return None

        return (x, y, w, h)

    def find_fish(self, img, bar):

        x, y, w, h = bar
        roi = img[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(
            gray,
            self.fish_template,
            cv2.TM_CCOEFF_NORMED
        )

        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val < 0.55:
            return None

        roi_x = max_loc[0] + self.fw // 2
        global_x = x + roi_x

        self.last_fish_x = global_x
        return global_x

    def find_zone(self, img, bar):

        x, y, w, h = bar
        roi = img[y:y+h, x:x+w]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Mavi olmayan
        mask = cv2.bitwise_not(blue_mask)

        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        valid = []
        for c in contours:
            area = cv2.contourArea(c)
            zx, zy, zw, zh = cv2.boundingRect(c)

            if 50 < area < 3000 and zw > 15:
                valid.append((c, zx, zw))

        if not valid:
            return None

        c, zx, zw = max(valid, key=lambda v: v[2])

        zone_center = zx + zw // 2

        return x + zone_center
    