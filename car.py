from ursina import *

class Car(Entity):
    def __init__(self, terrain_collider, **kwargs):
        super().__init__(**kwargs)

        name = 'car'
        self.hit_entity_centre = None
        self.hit_entity_front_left = None
        self.hit_entity_front = None
        self.visible_sensors = False
        self.autopilot = False

        self.road_check_distance = 1.0  # How far down to cast the ray
        self.terrain = terrain_collider # Model to use for detecting collisions

        # Load the 3D model directly on self
        model_path = 'assets/car.glb'
        self.model = model_path

        # Fallback for testing:
        if not Path(model_path).exists():
            print('Could not find model, using cube instead.')
            self.model = 'cube'

        self.scale = 1 # lower is smaller
        self.rotation_y = 90
        self.collider = 'box'

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

        # Check for collisions with the model
        self.check_road_surface()

        if self.autopilot:
            pass

    def check_road_surface(self):
        """
        Casts a ray downwards to detect the ground.
        This can be used to check for different surface types or to align the car to the ground normal.
        """
        # Do raycast from the left front
        front_left_offset = self.forward * (self.scale_z / 2)+Vec3(-0.5, 0, 0.5)
        raycast_start = self.position + front_left_offset

        hit_info = raycast(
            origin=raycast_start,
            direction=self.down,
            distance=self.road_check_distance,
            ignore=[self, ],
            traverse_target=self.terrain, # Only checks against the collision model
            debug=self.visible_sensors
        )
        if hit_info.hit:
            # The ray has hit something.
            self.hit_entity_front_left = hit_info.entity
        else:
            self.hit_entity_front_left = None

        # Do raycast from the front
        front_offset = self.forward * (self.scale_z / 2)
        raycast_start = self.position + front_offset

        hit_info = raycast(
            origin=raycast_start,
            direction=self.down,
            distance=self.road_check_distance,
            ignore=[self, ],
            traverse_target=self.terrain, # Only checks against the collision model
            # debug=self.visible_sensors
        )
        if hit_info.hit:
            # The ray has hit something.
            self.hit_entity_front = hit_info.entity
        else:
            self.hit_entity_front = None

        # Raycast from the centre
        ray_origin = self.world_position
        hit_info = raycast(
            origin=ray_origin,
            direction=self.down,
            distance=self.road_check_distance,
            ignore=[self, ],
            traverse_target=self.terrain, # Only checks against the collision model
            # debug=self.visible_sensors # One at a time
        )
        if hit_info.hit:
            # The ray has hit something.
            self.hit_entity_centre = hit_info.entity
        else:
            self.hit_entity_centre = None

    def hit_centre(self):
        self.hit_entity_centre.name

    def hit_front(self):
        self.hit_entity_front.name

    def show_sensor(self, v):
        self.visible_sensors = v

    def get_show_sensor(self):
        return self.visible_sensors

    def set_autopilot(self, v):
        self.autopilot = v

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
