from ursina import EditorCamera

class SmoothEditorCamera(EditorCamera):
    def __init__(self):
        super().__init__()
        self.rotation_speed = 100
        self.smooth_factor = 0.1

    def update(self):
        super().update()
        # Smooth out small rotation jitters
        if abs(self.rotation_x) < 0.1:
            self.rotation_x = 0
        if abs(self.rotation_y) < 0.1:
            self.rotation_y = 0
        if abs(self.rotation_z) < 0.1:
            self.rotation_z = 0