from ursina import *
from ursina.prefabs.editor_camera import EditorCamera

app = Ursina()

# Add a simple sky and ground for reference
Sky()
ground = Entity(model='plane', scale=100, color=color.gray, collider='box')

# Editor Camera
editor_camera = EditorCamera(rotation_smoothing=2, panning_speed=4)

# Load your GLB model (example: 'cube.glb' in the same folder)
model_name = 'assets/Models/GLB format_roads/track-road-wide.glb'

class grid (Entity):
    def buildGrid(self):
        self.grid_size = (5, 5)  # 5 x 5 grid
        self.grid_spacing = 2

        # Get all filenames ending with .glb
        assets_dir = 'assets/Models/GLB format_roads'
        glb_files = [f for f in os.listdir(assets_dir) if f.endswith('.glb')]
        track_files = [f for f in glb_files if 'track' in f.lower()]
        model_entities = []

#        for track_file in track_files:
#            print(f"Found track file: {track_file}")

        index = 0
        # Create a grid of model entities
        for x in range(self.grid_size[0]):
            for z in range(self.grid_size[1]):
                model_name = track_files[index]
                index = index + 1
                if (index == len(track_files)):
                    index = 0
                model_entity = Entity(
                    model=model_name,
                    position=(x * self.grid_spacing, 0.5, z * self.grid_spacing),
                    scale=1,
                    collider=None
                )
                print(f'model_entity: {model_entity.bounds.size}')
                model_entities.append(model_entity)
                # print(model_entity.bounds.size)  # Print the size of the model entity

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = 'plane'
        self.scale = 100
        self.color = color.gray
        self.collider = 'box'
        self.buildGrid()

gr = grid()

app.run()
