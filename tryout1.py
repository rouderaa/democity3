from ursina import *

if __name__ == "__main__":
    # Initialize the Ursina application
    app = Ursina()

    # --- Main window setup ---

    # Add an entity to the scene so we have something to look at
    Entity(model='cube', color=color.orange, scale=2)
    Entity(model='sphere', color=color.azure, x=3)
    Entity(model='plane', scale=10, texture='white_cube', texture_scale=(10, 10))


    # Add the movable camera to the main window
    # This provides the default camera controls
    EditorCamera()

    # Run the application
    app.run()