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
            # Make it invisible (optional - remove these lines if you want to see the colliders)
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
    x, z, y = car_entity.position
    position_display.text = f"position: ({x:.2f},{y:.2f})"
    hits_display.text = f"hits: {getattr(car_entity.hit_entity, 'name', '')}"

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
Sky()
ground = Entity(model='plane', name='ground', scale=100, color=color.rgb(32, 189, 28))

# Editor Camera
# editor_camera = EditorCamera(rotation_smoothing=2, panning_speed=4)
editor_camera = SmoothEditorCamera()
editor_camera.y = 10
editor_camera.x = -20
editor_camera.z = -15

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
    color=color.green,
    mode='wireframe',  # This enables wire rendering
    visible=False
)

# use the boxes in the model_colliders to create actual box colliders
make_colliders()

# Make the car
car_entity = Car(position=(0, 0, 0), terrain_collider=model_colliders_entity)

# define the status lines on the screen
position_display = Text(text='', position=window.top_left + Vec2(0.05, -0.05), scale=1.5)
hits_display = Text(text='', position=window.top_left + Vec2(0.05, -0.10), scale=1.5)

app.run()
