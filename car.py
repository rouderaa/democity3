from ursina import *

class Car(Entity):
    def __init__(self, terrain_collider, **kwargs):
        super().__init__(**kwargs)

        name = 'car'
        self.fl_hit = None
        self.f_hit = None
        self.fr_hit = None
        self.c_hit = None

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

    """
    Casts a ray downwards to detect the ground.
    """

    def probe(self, probe_offset, probe_postfix, show_probe):
        """
        Casts a ray from a point relative to the entity's position and rotation.

        :param probe_offset: A Vec3 representing the local offset from the entity's center.
        :param probe_postfix: A unique string/identifier for this specific probe.
        :param show_probe: A boolean to toggle the visibility of a debug line.
        """
        # --- 1. CORRECTLY CALCULATE THE RAYCAST ORIGIN IN WORLD SPACE ---
        # Use Ursina's built-in rotation methods
        # This rotates the offset vector by the entity's rotation
        r = self.forward * probe_offset.z + self.right * probe_offset.x + self.up * probe_offset.y
        raycast_start = self.world_position + r

        # if show_probe:
        #    print(f"{probe_postfix}: world_rotation {self.world_rotation} probe_offset {probe_offset} r {r} raycast_start {raycast_start}\n")

        # --- 2. USE THE ENTITY'S ROTATED "DOWN" VECTOR FOR THE DIRECTION ---
        # `self.down` is an automatically updated property in Ursina that gives the
        # entity's down direction in world space (e.g., if the entity is upside down, this points up).
        ray_direction = self.down

        # Perform the raycast
        hit_info = raycast(
            origin=raycast_start,
            direction=ray_direction,
            distance=self.road_check_distance,
            ignore=[self, ],
            traverse_target=self.terrain,  # Only checks against the collision model
            debug=False
        )

        # --- 3. UPDATE THE DEBUGGING VISUALIZATION ---
        if show_probe:
            # Use a unique key to find or create a reusable entity for the debug line
            probe_key = f"_probe_line_{probe_postfix}"

            # Create the probe line entity if it doesn't exist yet
            if not hasattr(self, probe_key):
                # The probe is a thin cube. Its length is along its y-axis by default.
                # We will set its y-scale dynamically to match the ray's length.
                setattr(self, probe_key, Entity(
                    model='cube',
                    color=color.red,
                    scale_x=0.02,
                    scale_z=0.02,
                    enabled=False
                ))

            probe_line = getattr(self, probe_key)

            # --- CORRECTLY POSITION, SCALE, AND ROTATE THE VISUAL PROBE ---
            # The center of the line is halfway between the start and the potential end point.
            line_center = raycast_start + (ray_direction * self.road_check_distance * 0.5)
            probe_line.position = line_center

            # Scale the probe's length (its y-axis) to match the raycast distance
            probe_line.scale_y = self.road_check_distance

            # Rotate the probe so its length (its local y-axis) aligns with the ray's direction.
            # Setting `world_up` tells Ursina to rotate the entity so its local `up` vector
            # points in the direction of `ray_direction`. Since our ray is pointing "down",
            # this correctly orients our line model.
            probe_line.world_up = ray_direction

            # Enable the probe and set its color based on whether it hit something
            probe_line.enabled = True
            probe_line.color = color.green if hit_info.hit else color.red
        else:
            # If not debugging, ensure all probe lines are hidden
            for attr_name in dir(self):
                if attr_name.startswith('_probe_line_'):
                    getattr(self, attr_name).enabled = False

        # Return the entity that was hit, or None if nothing was hit
        return hit_info.entity if hit_info.hit else None

    def check_road_surface(self):
        # Define offsets in the entity's local space.
        # The 'probe' function will handle transforming these into world space.
        # We assume local +Z is forward, and local +X is to the right.

        up_offset = 0.5
        # Offset for the front-left corner
        front_left_offset = Vec3(-0.75, up_offset, (self.scale_z / 2)+0.25)
        self.fl_hit = self.probe(front_left_offset, "fl", self.visible_sensors)

        # Offset for the center-front
        front_offset = Vec3(0, up_offset, self.scale_z / 2)
        self.f_hit = self.probe(front_offset, "f", self.visible_sensors)

        # Offset for the front-right corner
        front_right_offset = Vec3(0.75, up_offset, (self.scale_z / 2)+0.25)
        self.fr_hit = self.probe(front_right_offset, "fr", self.visible_sensors)

        # Offset for the entity's center (no offset)
        centre_offset = Vec3(0, up_offset, 0)
        self.c_hit = self.probe(centre_offset, "c", self.visible_sensors)

    def hit_centre(self):
        self.c_hit

    def hit_front(self):
        self.f_hit

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
