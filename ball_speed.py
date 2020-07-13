
import cv2
import math


class Ball:
    def __init__(self):
        self.ball_speed = 0
        self.ball_history = []

    def get_ball_speed(self, c1, c2):
        if self.is_ball_in_tolerance(c1, c2):
            self.ball_history.append((c1, c2))

            if len(self.ball_history) > 1:
                radius = abs(c1[0]-c2[0])/2
                real_radius = 0.11

                center_coordinates_start = (
                    int((c1[0]+c2[0])/2), int((c1[1]+c2[1])/2))
                center_coordinates_end = (
                    int((self.ball_history[0][0][0] +
                         self.ball_history[0][1][0]
                         )/2),
                    int((self.ball_history[0][0][1] +
                         self.ball_history[0][1][1])
                        / 2)
                )
                print(f"center_coordinates_start: {center_coordinates_start}")
                print(f"center_coordinates_end: {center_coordinates_end}")

                centers_distance = math.sqrt(
                    (center_coordinates_start[0] -
                     center_coordinates_end[0])**2
                    +
                    (center_coordinates_start[1] -
                     center_coordinates_end[1])**2,
                )

                real_distance = real_radius * centers_distance / radius
                speed = real_distance / (len(self.ball_history)/25)
                print(f"radius: {radius}")
                print(f"centers_distance: {centers_distance}")
                print(f"real_distance: {real_distance}")
                print(f"speed: {speed}")
                self.ball_speed = round(float(speed), 3)

        else:
            self.ball_history = [(c1, c2)]
            # self.ball_speed

        # return round(self.ball_speed, 2)
        return self.ball_speed

    def is_ball_in_tolerance(self, c1, c2):
        if len(self.ball_history) == 0:
            return False

        tolerance = 50
        prev_frames_window = 25

        points_to_check = prev_frames_window if len(
            self.ball_history) > prev_frames_window else len(self.ball_history)

        for i in range(points_to_check):
            if abs(c1[0]-self.ball_history[i][0][0]) < tolerance:
                return True
        return False

    def draw(self, img, c1, c2, color):
        ball_speed = self.get_ball_speed(c1, c2)

        center_coordinates = (int((c1[0]+c2[0])/2), int((c1[1]+c2[1])/2))
        radius = abs(c1[0]-c2[0])/2
        tickness = -1
        cv2.circle(img, center_coordinates, radius, color, tickness)

        upper_alpha = 1
        lower_alpha = .8
        for i, ball in enumerate(self.ball_history):
            overlay = img.copy()
            multiplier = 1 - (i / len(self.ball_history))
            alpha = lower_alpha + (upper_alpha - lower_alpha) * multiplier
            c1 = ball[0]
            c2 = ball[1]
            center_coordinates = (int((c1[0]+c2[0])/2), int((c1[1]+c2[1])/2))
            radius = abs(c1[0]-c2[0])/2
            cv2.circle(img, center_coordinates,
                       radius, color, -1)
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

            # img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        return img, ball_speed


def write_ball_speed(ball_speed, img):
    color = (255, 0, 0)

    label = f"v: {ball_speed} m/s"
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
    text_coordinates = (30, 30)
    text_c2 = text_coordinates[0] + \
        t_size[0], text_coordinates[1] + t_size[1] + 5

    cv2.rectangle(img, text_coordinates, text_c2, color, -1)
    cv2.putText(img, label, (text_coordinates[0], text_coordinates[1] + t_size[1] + 4),
                cv2.FONT_HERSHEY_PLAIN, 2, [225, 255, 255], 2)
