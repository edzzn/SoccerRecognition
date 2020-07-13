import numpy as np
import cv2
import time
import datetime
import imutils


class VideoIn():
    def __init__(self, running, queue, top=0, left=0, width=1200, height=675, hasTreadStarted=False, recording=False):
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

    def _processingFrame(self, frame, frame_counter):
        # try:
        img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        # print(f"fc: {frame_counter}")
        if (self.detector):
            img = self.detector.detect(
                img,
                frame_counter=frame_counter
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

        # if (isinstance(img, (np.ndarray, np.generic))):
        #     print('_processingFrame', img.shape)
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
                while(self.running):
                    # if frame_counter < 2073:
                    #     self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 2073)
                    #     frame_counter = 2073

                    if self.queue.qsize() < 10:
                        ret, frame = self.video_cap.read()
                        if ret == True:

                            frame = imutils.resize(frame, width=1200)
                            if (isinstance(frame, (np.ndarray, np.generic))):
                                # print(frame.shape)
                                self.width,  self.height, _ = frame.shape

                            self._processingFrame(frame, frame_counter)
                            frame_counter += 1
                        print(
                            f"{frame_counter}/{self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
                        if frame_counter == self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT):
                            frame_counter = 0  # Or whatever as long as it is the same as next line
                            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def _addToQueue(self, image):
        self.queue.put((image, None))

    def _record(self, image):
        self.img_counter += 1

        if (isinstance(image, (np.ndarray, np.generic))):
            print('_record', image.shape)
        if(self.writer):
            self.writer.write(image[..., :3])

    def start_record(self):

        filename = f'records/record-{self.counter}.avi'
        codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        framerate = 25
        resolution = (self.height, self.width)
        print(f"resolution {resolution}")
        # resolution = (1280, 720)
        # resolution = (1280, 720)
        self.writer = cv2.VideoWriter(filename, codec, framerate, resolution)
        self.counter += 1

    def _stop_recording(self):
        if(self.writer):
            self.writer.release()

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
