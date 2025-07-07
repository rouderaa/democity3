from ursina import *
from ursina.prefabs.editor_camera import EditorCamera
from smoothcamera import SmoothEditorCamera
from car import Car

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
ground = Entity(model='plane', scale=100, color=color.gray, collider='box')

# Editor Camera
# editor_camera = EditorCamera(rotation_smoothing=2, panning_speed=4)
editor_camera = SmoothEditorCamera()
editor_camera.y = 10
editor_camera.x = -20
editor_camera.z = -20

# Load your GLB model (example: 'cube.glb' in the same folder)
model_name = 'assets/Models/fullmodel.glb'
model_colliders_name = 'assets/Models/fullmodel_colliders.glb'

model_entity = Entity(
    model=model_name,
    position=(-40, 0, 1),
    scale=1,
    collider=None
)

# Note: y is vertical position in ursina
model_colliders_entity = Entity(
    model=model_colliders_name,
    position=(-40, 1, 1),
    scale=1,
    color=color.green,
    mode='wireframe',  # This enables wire rendering
    visible=False
)

car_entity = Car()

print('Model:', car_entity.model)
print('Model loaded:', car_entity.model in application.asset_folder.glob('**/*'))

app.run()
