import cv2
import numpy as np
import math


class LineasGol:
    def __init__(self):
        # self.it = 0
        self.fs = [0, 0]

        self.screen_size = {1645: 1649, 2273: 2278, 2863: 2868, 2881: 2900}
        self.horizontal_lines = []

    def add_linea_gol(self, frame, frame_counter):
        # self.it += 1

        frame = check_lines_goal(frame_counter, frame, self.screen_size,
                                 self.horizontal_lines, self.fs)

        return frame


def check_lines_goal(it, frame, screen_size, horizontal_lines, fs):

    if frame is None:
        return

    g_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = get_hsv_frame(frame)
    edges = cv2.Canny(result, 150, 80, 5)
    put_hough_lines(edges, frame)

    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    edgesOpening = cv2.Canny(opening, 150, 80, 5)
    put_hough_lines(edgesOpening, frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([33, 30, 62], dtype=np.uint8)
    upper_white = np.array([75, 255, 166], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([82, 0, 0], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    mask2 = cv2.inRange(hsv2, lower_white, upper_white)
    # Bitwise-AND mask and original image
    res2 = cv2.bitwise_and(frame, frame, mask=mask2)

    hsv3 = cv2.cvtColor(res2, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 0], dtype=np.uint8)
    upper_white = np.array([255, 45, 255], dtype=np.uint8)
    mask3 = cv2.inRange(hsv3, lower_white, upper_white)
    # Bitwise-AND mask and original image
    res3 = cv2.bitwise_and(res2, res2, mask=mask3)

    res4 = cv2.cvtColor(res3, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(res4, cv2.MORPH_OPEN, kernel)

    edges = cv2.Canny(opening, 150, 80, 5)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 90,
                            minLineLength=40, maxLineGap=5)
    vertical_lines = []
    if lines is not None:
        for i, line in enumerate(lines):
            x1, y1, x2, y2 = line[0]
            angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi
            if 87 < angle < 93:
                # print(angle)
                vertical_lines.append(lines)

    test_goal(vertical_lines, horizontal_lines, screen_size, it, frame, fs)

    # cv2.imshow('frame', frame)

    # cv2.imshow('edges', edges)
    # cv2.imshow('res2', result)
    # cv2.imshow('frame', frame)

    return frame


def vertical_hough_lines(edges, frame):
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 90,
                            minLineLength=40, maxLineGap=4)
    if lines is not None:
        for i, line in enumerate(lines):
            x1, y1, x2, y2 = line[0]
            angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi

            if angle < 95 and angle > 85:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)


def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def is_between(a, c, b):
    return distance(a, c) + distance(c, b) == distance(a, b)


def get_hsv_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([33, 30, 62], dtype=np.uint8)
    upper_white = np.array([75, 255, 166], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    blur = cv2.GaussianBlur(res, (15, 15), cv2.BORDER_DEFAULT)
    hsv2 = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_white2 = np.array([33, 30, 62], dtype=np.uint8)
    upper_white2 = np.array([75, 255, 166], dtype=np.uint8)
    mask2 = cv2.inRange(hsv2, lower_white2, upper_white2)
    # Bitwise-AND mask and original image
    return cv2.bitwise_and(res, res, mask=mask2)


def put_hough_lines(edges, frame):
    global horizontal_lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 90,
                            minLineLength=40, maxLineGap=5)
    if lines is not None:
        for i, line in enumerate(lines):
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)


def write_gol(frame):
    x = 10
    y = frame.shape[0] - 10
    # cv2.waitKey(200)
    cv2.putText(
        frame,  # numpy array on which text is written
        'GOL!',  # text
        (x, y),  # position at which writing has to start
        cv2.FONT_HERSHEY_SIMPLEX,  # font family
        4,  # font size
        (0, 0, 255, 0),  # font color
        3)  # font stroke


def test_goal(vertical_lines, horizontal_lines, screen_size, it, frame, fs):
    distance1 = 45
    distance2 = 90
    flag = True
    if len(horizontal_lines) > 0:
        for i, v in enumerate(vertical_lines):
            d1 = np.norm(np.cross(vertical_lines[i]) - v[0], v[1], vertical_lines[i]) / np.norm(
                vertical_lines[i] - v[0])
            error = 0.1
            if distance1 * error < d1 < distance1 * (error + 1):
                for j, h in enumerate(horizontal_lines):
                    d2 = np.norm(np.cross(horizontal_lines[j]) - h[0], h[1], horizontal_lines[j]) / np.norm(
                        horizontal_lines[j] - h[0])
                    error = 0.1
                    if distance2 * error < d2 < distance2 * (error + 1):
                        dist = distance(d1, d2)
                        flag = is_between(d1, d2, d2)
    try:
        if screen_size[it]:
            fs[0], fs[1] = it, screen_size[it]
    except:
        pass
    if fs[0] < it < fs[1]:
        write_gol(frame)


def nothing(a):
    pass
