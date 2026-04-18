import mss
import numpy as np
import cv2
import pygetwindow as gw


class Screen:
    def __init__(self, title):
        self.title = title
        self.sct = mss.mss()
        self.win = None

    def update_window(self):
        wins = gw.getWindowsWithTitle(self.title)
        if wins:
            self.win = wins[0]
        else:
            self.win = None

    def grab(self):
        self.update_window()

        if self.win is None or self.win.isMinimized:
            return None

        x, y = self.win.left, self.win.top
        w, h = self.win.width, self.win.height

        if w <= 0 or h <= 0:
            return None

        monitor = {
            "left": x,
            "top": y,
            "width": w,
            "height": h
        }

        img = self.sct.grab(monitor)

        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        return img
