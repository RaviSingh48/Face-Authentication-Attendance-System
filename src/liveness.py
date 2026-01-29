class HeadTurnChecker:
    def __init__(self):
        self.initial_x = None
        self.moved_left = False
        self.moved_right = False

    def update(self, face_x, frame_width):
        face_center_x = face_x

        if self.initial_x is None:
            self.initial_x = face_center_x
            return False

        # movement threshold (pixels)
        MOVE_THRESHOLD = 20

        if face_center_x < self.initial_x - MOVE_THRESHOLD:
            self.moved_left = True

        if face_center_x > self.initial_x + MOVE_THRESHOLD:
            self.moved_right = True

        return self.moved_left and self.moved_right

    def reset(self):
        self.initial_x = None
        self.moved_left = False
        self.moved_right = False
