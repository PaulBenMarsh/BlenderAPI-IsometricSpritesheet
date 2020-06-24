

class OutputSettings:
    
    from pathlib import Path
    
    output_path = Path("C:/users/studio/desktop/frame_renders")
    
    scene_name = "scene"
    action_name = "idle"

    number_of_directions = 8
    
    file_format = "PNG"

    frame_file_name_prefix = "frame"
    composite_file_name_prefix = "spritesheet"
    
    number_of_direction_digits = 3
    number_of_frame_digits = 4


def render_frames():
    import bpy
    from math import degrees, radians

    deg_per_direction = 360 / OutputSettings.number_of_directions

    scene = bpy.data.scenes[OutputSettings.scene_name]
    scene.render.image_settings.file_format = OutputSettings.file_format
    
    bpy.data.objects["armature"].animation_data.action = bpy.data.actions.get(OutputSettings.action_name)

    origin = bpy.data.objects["origin"]

    for direction_number in range(0, OutputSettings.number_of_directions):

        angle_deg = (direction_number - 3) * deg_per_direction

        print(f"Rotating camera (direction number: {direction_number})...")

        origin.rotation_euler.z = radians(angle_deg)

        print(f"Camera angle: {degrees(origin.rotation_euler.z)}")

        print(f"Rendering frames (direction number: {direction_number})...\n")
        
        scene.render.filepath = str(OutputSettings.output_path.joinpath(f"{OutputSettings.frame_file_name_prefix}_{OutputSettings.action_name}_{str(direction_number).zfill(OutputSettings.number_of_direction_digits)}_"))
        bpy.ops.render.render(scene=OutputSettings.scene_name, animation=True, write_still=False)

    origin.rotation_euler.z = 0.0
    print("All frames have been rendered")

def generate_composite():
    
    import bpy
    from PIL import Image
    from itertools import islice
    
    image_lists = []
    for direction_digits in [str(direction_number).zfill(OutputSettings.number_of_direction_digits) for direction_number in range(OutputSettings.number_of_directions)]:
        image_paths = sorted(OutputSettings.output_path.glob(f"{OutputSettings.frame_file_name_prefix}_{OutputSettings.action_name}_{direction_digits}_{'[0-9]'*OutputSettings.number_of_frame_digits}.{OutputSettings.file_format.lower()}"))
        image_lists.append(list(map(Image.open, image_paths)))
    
    assert image_lists
    
    scene = bpy.data.scenes[OutputSettings.scene_name]
    action = bpy.data.actions.get(OutputSettings.action_name)
    
    number_of_rows = OutputSettings.number_of_directions
    number_of_columns = int(action.frame_range[1] - 1)
    
    composite_width = scene.render.resolution_x * number_of_columns
    composite_height = scene.render.resolution_y * number_of_rows
    
    composite = Image.new("RGBA", (composite_width, composite_height))
    
    for y_offset, direction in enumerate(image_lists):
        for x_offset, frame in enumerate(direction):
            composite.paste(frame, (x_offset * scene.render.resolution_x, y_offset * scene.render.resolution_y))
            # frame.close()
    composite.save(str(OutputSettings.output_path.joinpath(f"{OutputSettings.composite_file_name_prefix}_{action.name}_{number_of_columns}x{number_of_rows}.{OutputSettings.file_format.lower()}")), OutputSettings.file_format)
    
    print("Composite image has been generated")


def main():

    render_frames()
    
    generate_composite()


if __name__ == "__main__":
    main()
