from ui_widgets import OwnImageWidget
from video_input import VideoIn
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import cv2
import numpy as np
import threading
import time
import queue as Queue
from detector import Detector
from pathlib import Path
import time

capture_thread = None
VIDEO_NAME = './b_r.mp4'
VIDEO_FPS = 25

q = Queue.Queue()
video_in = VideoIn(False, q)
canny_detector = Detector()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('tracker.ui', self)

        self.startButton.clicked.connect(self.start_clicked)
        self.recordButton.clicked.connect(self.record_clicked)
        self.tagsButton.clicked.connect(self.tags_clicked)
        self.cordenatesButton.clicked.connect(self.cordenates_clicked)
        self.screenshotButton.clicked.connect(self.screenshot_clicked)
        self.trackButton.clicked.connect(self.track_clicked)

        self.ImgWidget = OwnImageWidget(self.ImgWidget)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000/VIDEO_FPS)

    def start_clicked(self):
        global video_in

        if (not video_in.hasTreadStarted):
            video_in.set_source(VIDEO_NAME)
            capture_thread.start()
            video_in.hasTreadStarted = True

        if (video_in.running):
            video_in.running = False
            self.startButton.setText('Iniciar')
            self.startButton.setChecked(False)
        else:
            video_in.running = True
            self.startButton.setText('Pausar')
            self.startButton.setChecked(True)

    def record_clicked(self):
        global video_in
        if (not self.recordButton.isChecked()):
            self.recordButton.setText('Grabar')
            self.recordButton.setChecked(False)
            video_in.recording = False
            video_in.stop()

        else:
            self.recordButton.setText('Detener')
            self.recordButton.setChecked(True)
            video_in.recording = True

            video_in.start_record()

    def track_clicked(self):
        global video_in
        global canny_detector

        if (not self.trackButton.isChecked()):
            video_in.setDetector(None)
            self.trackButton.setChecked(False)
        else:
            self.trackButton.setChecked(True)
            video_in.setDetector(canny_detector)

    def tags_clicked(self):
        global canny_detector
        if (not self.tagsButton.isChecked()):
            self.tagsButton.setChecked(False)
            canny_detector.showTags = False
        else:
            self.tagsButton.setChecked(True)
            canny_detector.showTags = True

    def cordenates_clicked(self):
        global canny_detector
        if (not self.cordenatesButton.isChecked()):
            self.cordenatesButton.setChecked(False)
            canny_detector.showCordenates = False
        else:
            self.cordenatesButton.setChecked(True)
            canny_detector.showCordenates = True

    def screenshot_clicked(self):
        global video_in
        video_in.take_screenshot()

    def update_frame(self):
        if not q.empty():
            global video_in

            frame, *debug = q.get()

            image = self._np_image_to_q_image(frame)
            self.ImgWidget.setImage(image)

    def _np_image_to_q_image(self, image):
        global video_in

        window_width = video_in.width
        window_height = video_in.height

        img_height, img_width, _img_colors = image.shape
        scale_w = float(window_width) / float(img_width)
        scale_h = float(window_height) / float(img_height)
        scale = min([scale_w, scale_h])

        if scale == 0:
            scale = 1

        image = cv2.resize(image, None, fx=scale, fy=scale,
                           interpolation=cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, bpc = image.shape
        bytes_per_line = bpc * width
        q_image = QtGui.QImage(image.data, width, height,
                               bytes_per_line, QtGui.QImage.Format_RGB888)
        return q_image

    def closeEvent(self, event):
        global video_in
        video_in.running = False
        video_in.stop()


capture_thread = threading.Thread(
    target=video_in.grab
)

# Iniciar instancia de QT
app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.setWindowTitle('Soccer Detection')
window.show()
app.exec_()
