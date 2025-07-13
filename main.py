from ursina import *
from smoothcamera import SmoothEditorCamera
from car import Car

def print_tree(entity, indent=0):
    print(' ' * indent + f'{entity.name} ({entity.__class__.__name__})')
    for child in entity.children:
        print_tree(child, indent + 2)


# Create box colliders for each child
def make_colliders():
    colliders = []

    for child in model_colliders_entity.model.children:
        # print(f"Creating collider for: {child.name}")

        # Create a box collider entity
        collider = Entity(
            name=f"{child.name}",
            model='cube',
            # Get transform from the Panda3D NodePath
            position=child.getPos(),
            rotation=child.getHpr(),
            scale=child.getScale(),
            visible=False,
            # Or make it semi-transparent for debugging
            # color=color.red,
            # alpha=0.3,
            # Set up collision
            collider='box'
        )

        # Store reference to the collider
        colliders.append(collider)
        # set parent
        collider.parent = model_colliders_entity

    print(f"Created {len(colliders)} box colliders")

def update():
    cam_pos = editor_camera.position
    cam_rot = editor_camera.rotation
    zoom_distance = distance(camera.world_position, editor_camera.world_position)
    cam_display.text = f"cam: ({cam_pos.x:.2f},{cam_pos.y:.2f},{cam_pos.z:.2f}) ({editor_camera.rotation_x:.2f},{editor_camera.rotation_y:.2f},{editor_camera.rotation_z:.2f}) {zoom_distance:.2f}"
    x, z, y = car_entity.position
    position_display.text = f"position: ({x:.2f},{y:.2f})"
    hits_display.text = \
        f"hits: c:{getattr(car_entity.c_hit, 'name', '')} fl:{getattr(car_entity.fl_hit, 'name', '')} f:{getattr(car_entity.f_hit, 'name', '')} fr:{getattr(car_entity.fr_hit, 'name', '')}"
    ground.visible = not car_entity.get_show_sensor()
    model_colliders_entity.visible = not ground.visible
    sky.visible = ground.visible

def input(key):
    """Handle key press and release events"""
    if key == 'w':
        car_entity.move_forward(True)
    elif key == 'w up':
        car_entity.move_forward(False)

    elif key == 's':
        car_entity.move_backward(True)
    elif key == 's up':
        car_entity.move_backward(False)

    elif key == 'd':
        car_entity.turn_left(True)
    elif key == 'd up':
        car_entity.turn_left(False)

    elif key == 'a':
        car_entity.turn_right(True)
    elif key == 'a up':
        car_entity.turn_right(False)

    elif key == 't':
        car_entity.show_sensor(True)
    elif key == 'g':
        car_entity.show_sensor(False)

    elif key == 'z':
        car_entity.set_autopilot(True)
    elif key == 'x':
        car_entity.set_autopilot(False)


# app = Ursina()
app = Ursina(
    title='City demo',
    borderless=False,
    fullscreen=False,
    size=(1920, 1080),
    vsync=True,
    multisamples=4  # This enables antialiasing (MSAA)
)

# Add a simple sky and ground for reference
sky = Sky()
ground = Entity(model='plane', name='ground', scale=100, color=color.rgb(32, 189, 28))

# Load your GLB model (example: 'cube.glb' in the same folder)
model_name = 'assets/Models/fullmodel.glb'
model_colliders_name = 'assets/Models/fullmodel_colliders.glb'

model_entity = Entity(
    model=model_name,
    position=(0, 0, 0),
    scale=1,
    collider=None
)

# Note: y is vertical position in ursina
model_colliders_entity = Entity(
    model=model_colliders_name,
    position=(0, 0, 0),
    scale=1,
    color=color.cyan,
    mode='wireframe',  # This enables wire rendering
    visible=False
)

# use the boxes in the model_colliders to create actual box colliders
make_colliders()

# Make the car
car_pos=(-30.54, 0, 22.11)
car_entity = Car(position=car_pos, terrain_collider=model_colliders_entity)

# Editor Camera
# editor_camera = EditorCamera(rotation_smoothing=2, panning_speed=4)
editor_camera = SmoothEditorCamera()
editor_camera.y = 5
editor_camera.x = -20
editor_camera.z = -10

# Let camera look down at car
d = 10
editor_camera.position = (car_pos[0], car_pos[1] + d, car_pos[2])
# Set rotation to look straight down
editor_camera.rotation = (90, 0, 0)  # 90 degrees pitch to look down


# define the status lines on the screen
cam_display = Text(text='', position=window.top_left + Vec2(0.05, -0.0), scale=1.5)
position_display = Text(text='', position=window.top_left + Vec2(0.05, -0.05), scale=1.5)
hits_display = Text(text='', position=window.top_left + Vec2(0.05, -0.10), scale=1.5)

app.run()
