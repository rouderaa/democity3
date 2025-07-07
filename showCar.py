from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.editor_camera import EditorCamera
import math


class Car:
    def __init__(self, position=(0, 0, 0), **kwargs):
        # Create the main car entity
        self.entity = Entity(
            model='assets/car.glb',
            color=color.white,
            scale=1,
            position=position
        )

        # Car physics properties
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 20
        self.deceleration = 15
        self.turn_speed = 0
        self.max_turn_speed = 100
        self.turn_acceleration = 150

        # Apply any additional kwargs to the entity
        for key, value in kwargs.items():
            if hasattr(self.entity, key):
                setattr(self.entity, key, value)
            else:
                setattr(self, key, value)

    def move_forward(self, dt):
        """Move the car forward"""
        self.speed = min(self.speed + self.acceleration * dt, self.max_speed)

    def move_backward(self, dt):
        """Move the car backward"""
        self.speed = max(self.speed - self.acceleration * dt, -self.max_speed * 0.5)

    def turn_left(self, dt):
        """Turn the car left"""
        if abs(self.speed) > 0.1:  # Only turn when moving
            turn_factor = self.speed / self.max_speed
            self.turn_speed = min(self.turn_speed + self.turn_acceleration * dt, self.max_turn_speed)
            self.entity.rotation_y += self.turn_speed * turn_factor * dt

    def turn_right(self, dt):
        """Turn the car right"""
        if abs(self.speed) > 0.1:  # Only turn when moving
            turn_factor = self.speed / self.max_speed
            self.turn_speed = min(self.turn_speed + self.turn_acceleration * dt, self.max_turn_speed)
            self.entity.rotation_y -= self.turn_speed * turn_factor * dt

    def apply_friction(self, dt):
        """Apply friction to gradually stop the car"""
        if self.speed > 0:
            self.speed = max(0, self.speed - self.deceleration * dt)
        elif self.speed < 0:
            self.speed = min(0, self.speed + self.deceleration * dt)

        # Apply turning friction
        self.turn_speed = max(0, self.turn_speed - self.turn_acceleration * dt * 2)

    def update(self):
        """Update car physics and movement"""
        dt = time.dt

        # Handle input
        if held_keys['w'] or held_keys['up arrow']:
            self.move_forward(dt)
        elif held_keys['s'] or held_keys['down arrow']:
            self.move_backward(dt)
        else:
            self.apply_friction(dt)

        if held_keys['a'] or held_keys['left arrow']:
            self.turn_left(dt)
        elif held_keys['d'] or held_keys['right arrow']:
            self.turn_right(dt)
        else:
            self.turn_speed = max(0, self.turn_speed - self.turn_acceleration * dt * 2)

        # Move the car based on its current speed and rotation
        forward_direction = Vec3(
            math.sin(math.radians(self.entity.rotation_y)),
            0,
            math.cos(math.radians(self.entity.rotation_y))
        )

        self.entity.position += forward_direction * self.speed * dt


# Example usage
if __name__ == "__main__":
    # Initialize Ursina
    app = Ursina()

    # Create a simple ground
    ground = Entity(
        model='cube',
        color=color.green,
        scale=(100, 1, 100),
        position=(0, -1, 0)
    )

    # Create the car
    car = Car(position=(0, 0, 0))

    # Set up camera modes
    editor_camera = EditorCamera()
    follow_camera = Entity()

    # Configure follow camera
    follow_camera.parent = car.entity
    follow_camera.position = (0, 5, -10)
    follow_camera.rotation_x = -15

    # Start with editor camera
    camera.parent = scene
    camera.position = (10, 10, 10)
    camera.look_at(car.entity)

    # Camera switching variables
    camera_mode = 'editor'  # 'editor' or 'follow'


    def switch_camera():
        global camera_mode
        if camera_mode == 'editor':
            camera_mode = 'follow'
            camera.parent = follow_camera
            camera.position = (0, 0, 0)
            camera.rotation = (0, 0, 0)
            editor_camera.enabled = False
        else:
            camera_mode = 'editor'
            camera.parent = scene
            camera.position = follow_camera.world_position
            camera.rotation = follow_camera.world_rotation
            editor_camera.enabled = True


    # Add camera switch functionality
    def input(key):
        if key == 'c':
            switch_camera()


    # Add some lighting
    DirectionalLight(
        parent=scene,
        y=2,
        z=3,
        shadows=True
    )

    # Instructions text
    instructions = Text(
        'WASD or Arrow Keys to drive the car\nW/Up: Forward\nS/Down: Backward\nA/Left: Turn Left\nD/Right: Turn Right\nC: Switch Camera (Editor/Follow)',
        position=(-0.8, 0.4),
        scale=0.8,
        color=color.white
    )

    # Optional: Add some reference objects
    for i in range(5):
        for j in range(5):
            if i != 2 or j != 2:  # Don't place where car starts
                cube = Entity(
                    model='cube',
                    color=color.orange,
                    scale=0.5,
                    position=(i * 10 - 20, 0, j * 10 - 20)
                )

    # Run the application
    app.run()