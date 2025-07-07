from ursina import *


class Car(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load the 3D model directly on self
        # Debug path
        model_path = 'assets/car.glb'
        print('Looking for:', Path(model_path).resolve())
        print('Exists:', Path(model_path).exists())

        self.model = model_path

        # Fallback for testing:
        if not Path(model_path).exists():
            print('Could not find model, using cube instead.')
            self.model = 'cube'

        self.scale = 2
        self.rotation_y = 90
        self.collider = 'box'  # or None if you don’t need collisions

        # Car properties
        self.speed = 5  # Movement speed
        self.rotation_speed = 90  # Rotation speed in degrees per second

        # Movement state
        self.is_moving_forward = False
        self.is_moving_backward = False
        self.is_turning_left = False
        self.is_turning_right = False

    def input(self, key):
        """Handle key press and release events"""
        if key == 'w':
            self.is_moving_forward = True
        elif key == 'w up':
            self.is_moving_forward = False

        elif key == 's':
            self.is_moving_backward = True
        elif key == 's up':
            self.is_moving_backward = False

        elif key == 'd':
            self.is_turning_left = True
        elif key == 'd up':
            self.is_turning_left = False

        elif key == 'a':
            self.is_turning_right = True
        elif key == 'a up':
            self.is_turning_right = False

    def update(self):
        """Update car movement every frame"""
        # Handle forward/backward movement
        if self.is_moving_forward:
            self.position += self.forward * self.speed * time.dt
        elif self.is_moving_backward:
            self.position += self.back * self.speed * time.dt

        # Handle left/right turning
        if self.is_turning_left:
            self.rotation_y += self.rotation_speed * time.dt
        elif self.is_turning_right:
            self.rotation_y -= self.rotation_speed * time.dt


# Example usage:
if __name__ == "__main__":
    app = Ursina()

    # Create a car instance
    car = Car(position=(0, 0, 0))

    # Set up camera to follow the car
    camera.parent = car
    camera.position = (0, 5, -15)
    camera.rotation_x = 20

    # Add some basic lighting
    DirectionalLight(direction=(1, -1, 1), color=color.white)

    # Add a ground plane for reference
    ground = Entity(model='plane', scale=50, color=color.gray, texture='white_cube', collider='box')

    app.run()
