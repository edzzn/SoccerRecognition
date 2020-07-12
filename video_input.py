import numpy as np
import cv2
import time
import datetime


class VideoIn():
    def __init__(self, running, queue, top=0, left=0, width=800, height=500, hasTreadStarted=False, recording=False):
        self.running = running
        self.recording = recording
        self.queue = queue
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.hasTreadStarted = hasTreadStarted
        self.writer = None
        self.counter = 0
        self.img_counter = 0
        self.should_take_screenshot = False
        self.detector = None
        self.source = ''
        self.video_cap = None

    def _processingFrame(self, frame):
        # try:
        img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        if (self.detector):
            img = self.detector.detect(
                img,
            )
        # if (img.shape)
        # print(img.shape[2])

        # height, width = img.shape[:2]
        # if (self.width != width or self.height != height):
        #     # self.width = 100
        #     # print(width)
        #     self.width = width
        #     self.height = height

        self._addToQueue(img)
        if(self.recording):
            self._record(img)
        if(self.should_take_screenshot):
            self._take_screenshot(img)

        # except:
        #     self.running = False
        #     print("An exception occurred")

    def set_source(self, new_source):
        print(f"set_source(self, new_source): {new_source}")
        # Close video capture
        self.source = new_source
        if(self.video_cap):
            self.video_cap.release()

    def grab(self):
        while True:
            print(f"Showing: {self.source} - {datetime.datetime.now()}")
            self.video_cap = cv2.VideoCapture(self.source)
            if (not self.video_cap.isOpened()):
                print("Error en cargar archivo")
            frame_counter = 0
            while(self.video_cap.isOpened()):
                if (self.width != self.video_cap.get(3) or self.height != self.video_cap.get(4)):
                    self.width = int(self.video_cap.get(3) * 0.80)
                    self.height = int(self.video_cap.get(4) * 0.80)

                while(self.running):
                    if self.queue.qsize() < 10:
                        ret, frame = self.video_cap.read()
                        if ret == True:
                            frame_counter += 1
                            self._processingFrame(frame)

                        if frame_counter == self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT):
                            frame_counter = 0  # Or whatever as long as it is the same as next line
                            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def _addToQueue(self, image):
        self.queue.put((image, None))

    def _record(self, image):
        self.img_counter += 1
        if(self.writer):
            self.writer.write(image[..., :3])

    def start_record(self):

        filename = f'records/record-{self.counter}.avi'
        codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        framerate = 25
        # resolution = (self.width,  self.height)
        resolution = (1280, 720)
        self.writer = cv2.VideoWriter(filename, codec, framerate, resolution)
        self.counter += 1

    def stop(self):
        if(self.writer):
            self.writer.release()

        if(self.video_cap):
            self.video_cap.release()

    def _take_screenshot(self, image):
        cv2.imwrite(
            f'records/screenshot-{self.img_counter}.jpg', image)
        self.img_counter += 1
        self.should_take_screenshot = False

    def take_screenshot(self):
        self.should_take_screenshot = True

    def setDetector(self, detector):
        self.detector = detector
