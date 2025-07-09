from ursina import *


class Car(Entity):
    def __init__(self, terrain_collider, **kwargs):
        super().__init__(**kwargs)

        name = 'car'
        self.hit_entity = None
        self.visible_sensors = False

        self.road_check_distance = 1.0  # How far down to cast the ray
        self.terrain = terrain_collider

        # Load the 3D model directly on self
        model_path = 'assets/car.glb'
        # print('Looking for:', Path(model_path).resolve())
        # print('Exists:', Path(model_path).exists())
        self.model = model_path

        # Fallback for testing:
        if not Path(model_path).exists():
            print('Could not find model, using cube instead.')
            self.model = 'cube'

        self.scale = 2
        self.rotation_y = 90
        self.collider = 'box'  # or None if you don’t need collisions

        # Car properties
        self.speed = 1  # Movement speed
        self.rotation_speed = 90  # Rotation speed in degrees per second

        # Movement state
        self.is_moving_forward = False
        self.is_moving_backward = False
        self.is_turning_left = False
        self.is_turning_right = False

    def move_forward(self, m):
        self.is_moving_forward = m

    def move_backward(self, m):
        self.is_moving_backward = m

    def turn_left(self, r):
        self.is_turning_left = r

    def turn_right(self, r):
        self.is_turning_right = r

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

        self.check_road_surface()

    def check_road_surface(self):
        """
        Casts a ray downwards to detect the ground.
        This can be used to check for different surface types or to align the car to the ground normal.
        """
        ray_origin = self.world_position

        # Instead of searching the whole scene, this tells the raycast to ONLY
        # check for hits against the entity stored in self.terrain.
        # This is more efficient and solves the problem of detecting the correct ground mesh.
        hit_info = raycast(
            origin=ray_origin,
            direction=self.down,
            distance=self.road_check_distance,
            ignore=[self, ],
            traverse_target=self.terrain, # Only check against the terrain!
            debug=self.visible_sensors
        )
        if hit_info.hit:
            # The ray has hit something.
            self.hit_entity = hit_info.entity
        else:
            self.hit_entity = None

    def hit(self):
        self.hit_entity.name

    def show_sensor(self, v):
        self.visible_sensors = v

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
