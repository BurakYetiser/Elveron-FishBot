import time
import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from screen import Screen
from vision import Vision
from space_input import press_space
import win32gui

class Worker(QThread):

    frame_signal = pyqtSignal(object)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.running = False
        self.window_title = "Elveron"

        self.last_space_time = 0
        self.space_cooldown = 0.16  

        self.collision_threshold = 3  
        self.fish_last_seen = time.time()
        self.fish_timeout = 3.0
        self.last_space_time = 0
        self.wait_after_close = False
        self.bar_close_time = 0
        self.waiting_for_bar = False
        self.bar_open_time = 0

    def is_game_active(self):
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0:
            return False

        title = win32gui.GetWindowText(hwnd)
        return self.window_title.lower() in title.lower()



    def run(self):

        self.running = True
        screen = Screen("Elveron")
        vision = None

        self.status_signal.emit("Oyun bekleniyor...")

        while self.running:

            img = screen.grab()
            if not self.is_game_active():
                self.status_signal.emit("Oyun aktif değil")
                self.msleep(500)
                continue

            if img is None:
                self.msleep(50)
                continue

            if vision is None:
                try:
                    vision = Vision()
                    self.status_signal.emit("Fishing Started")
                except Exception as e:
                    self.status_signal.emit(f"Vision Hatası: {e}")
                    self.msleep(1000)
                    continue

            current_time = time.time()
            bar = vision.get_bar(img)



            bar = vision.get_bar(img)
            if self.waiting_for_bar:
                if current_time - self.bar_open_time < 0.15:
                    self.msleep(5)
                    continue
                else:
                    self.waiting_for_bar = False

            fish_x = None
            zone_x = None

            if bar is not None:
                fish_x = vision.find_fish(img, bar)
                zone_x = vision.find_zone(img, bar)
            current_time = time.time()

            if fish_x is not None:
                self.fish_last_seen = current_time
                self.waiting_for_bar = False

            if current_time - self.fish_last_seen > self.fish_timeout:
                if not self.waiting_for_bar:
                    if current_time - self.last_space_time > self.space_cooldown:
                        press_space()
                        self.last_space_time = current_time
                        self.waiting_for_bar = True
                        self.bar_open_time = current_time
                        self.fish_last_seen = current_time
                        self.status_signal.emit("Balık yok → Bar açılıyor")
                    continue



            bx, by, bw, bh = bar

            fish_x = vision.find_fish(img, bar)
            zone_x = vision.find_zone(img, bar)

            if fish_x is not None and zone_x is not None:
                
                if abs(fish_x - zone_x) <= 2:

                    press_space()
                    self.status_signal.emit("MERKEZ ÇAKIŞTI")
                    self.msleep(1000)
                    continue

            bx, by, bw, bh = bar

            fish_x = vision.find_fish(img, bar)
            zone_x = vision.find_zone(img, bar)

            if fish_x is not None and zone_x is not None:

                if abs(fish_x - zone_x) <= self.collision_threshold:
                    
                    if current_time - self.last_space_time > self.space_cooldown:
                        self.msleep(6)
                        press_space()
                        self.last_space_time = current_time

                        self.wait_after_close = True
                        self.bar_close_time = current_time

            roi = img[by:by+bh, bx:bx+bw]

            if fish_x is not None:
                cv2.circle(roi, (fish_x - bx, bh // 2), 5, (0,255,0), -1)

            if zone_x is not None:
                cv2.circle(roi, (zone_x - bx, bh // 2), 5, (0,0,255), -1)

            self.frame_signal.emit(roi)

            self.msleep(8)  

        self.status_signal.emit("Fishing Stopped")

    def stop(self):
        self.running = False
