
class Ball:
    def __init__(self):
        self.ball_speed = 0
        self.ball_history = []

    def get_ball_speed(self, c1, c2):
        if self.is_ball_in_tolerance(c1, c2):
            print('ball_speed = 1000')
            self.ball_history.append((c1, c2))
            print('self.ball_history', len(self.ball_history))
            if (self.ball_speed == 0):
                self.ball_speed = len(self.ball_history)
            self.ball_speed += len(self.ball_history) * .03

        else:
            self.ball_history = [(c1, c2)]
            self.ball_speed = 0

        return self.ball_speed

    def is_ball_in_tolerance(self, c1, c2):
        if len(self.ball_history) == 0:
            return False

        tolerance = 20
        prev_frames_window = 25

        points_to_check = prev_frames_window if len(
            self.ball_history) > prev_frames_window else len(self.ball_history)

        for i in range(points_to_check):
            if abs(c1[0]-self.ball_history[i][0][0]) < tolerance:
                return True
        return False
