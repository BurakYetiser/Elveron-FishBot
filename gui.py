import cv2
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame,
    QTextEdit, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from worker import Worker

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FishBotV1")
        self.resize(1000, 700)
        self.setMinimumSize(900, 600)

        self.worker = None
        self.setup_ui()

    def setup_ui(self):

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e2e8f0;
                font-family: Segoe UI;
            }

            QFrame {
                background-color: #1e293b;
                border-radius: 12px;
                padding: 12px;
            }

            QPushButton {
                background-color: #2563eb;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                color: white;
            }

            QPushButton:hover {
                background-color: #3b82f6;
            }

            QPushButton#stop {
                background-color: #dc2626;
            }

            QPushButton#stop:hover {
                background-color: #ef4444;
            }

            QTextEdit {
                background-color: #0f172a;
                border-radius: 8px;
                padding: 8px;
            }
        """)

        main_layout = QVBoxLayout()


        top_card = QFrame()
        top_layout = QHBoxLayout()

        self.status_label = QLabel("Status: Idle")
        self.fps_label = QLabel("FPS: 0")


        top_layout.addWidget(self.status_label)
        top_layout.addStretch()
        top_layout.addWidget(self.fps_label)
        top_layout.addSpacing(20)

        top_card.setLayout(top_layout)
        main_layout.addWidget(top_card)


        video_card = QFrame()
        video_layout = QVBoxLayout()

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setMinimumHeight(300)

        video_layout.addWidget(self.video_label)
        video_card.setLayout(video_layout)

        main_layout.addWidget(video_card)


        control_card = QFrame()
        control_layout = QHBoxLayout()

        self.start_btn = QPushButton("START")
        self.stop_btn = QPushButton("STOP")
        self.stop_btn.setObjectName("stop")

        self.debug_checkbox = QCheckBox("Debug Overlay")

        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.debug_checkbox)

        control_card.setLayout(control_layout)
        main_layout.addWidget(control_card)


        log_card = QFrame()
        log_layout = QVBoxLayout()

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(180)

        log_layout.addWidget(QLabel("Logs"))
        log_layout.addWidget(self.log_box)

        log_card.setLayout(log_layout)
        main_layout.addWidget(log_card)

        self.setLayout(main_layout)


        self.start_btn.clicked.connect(self.start_bot)
        self.stop_btn.clicked.connect(self.stop_bot)

    def start_bot(self):
        if self.worker is None:
            self.worker = Worker()
            self.worker.status_signal.connect(self.update_status)
            self.worker.frame_signal.connect(self.update_frame)

            self.worker.debug_mode = self.debug_checkbox.isChecked()

            self.worker.start()
            self.log_box.append("Bot Started")

    def stop_bot(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait(2000)
            self.worker = None
            self.log_box.append("Bot Stopped")

    def update_status(self, text):
        if text.startswith("FPS"):
            self.fps_label.setText(text)
        else:
            self.status_label.setText(f"Status: {text}")
            self.log_box.append(text)

    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        qt_img = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qt_img)
        scaled = pixmap.scaled(
            self.video_label.width(),
            self.video_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

        self.video_label.setPixmap(scaled)