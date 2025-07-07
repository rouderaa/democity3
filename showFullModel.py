from ursina import *
from ursina.prefabs.editor_camera import EditorCamera

app = Ursina()

# Add a simple sky and ground for reference
Sky()
ground = Entity(model='plane', scale=100, color=color.gray, collider='box')

# Editor Camera
editor_camera = EditorCamera(rotation_smoothing=2, panning_speed=4)

# Load your GLB model (example: 'cube.glb' in the same folder)
model_name = 'assets/Models/fullmodel.glb'

model_entity = Entity(
    model=model_name,
    position=(-40, 0, 1),
    scale=1,
    collider=None
)

app.run()
