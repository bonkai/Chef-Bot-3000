import bpy
import os
import math

def clear_scene():
    """Clears the default Blender scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def import_glb(glb_filepath):
    """Imports a GLB file into the Blender scene."""
    bpy.ops.import_scene.gltf(filepath=glb_filepath)

def setup_camera_and_lighting(model_object):
    """Sets up the camera and basic lighting."""
    # Camera setup
    camera_data = bpy.data.cameras.new(name="Camera")
    camera_object = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera_object)
    bpy.context.scene.camera = camera_object

    # Position camera a bit back and above, looking at the origin initially
    camera_object.location = (2, -2, 2)  # Initial position, adjust as needed
    camera_object.rotation_euler = (math.radians(60), 0, math.radians(45)) # Initial rotation

    # Make camera look at the model (or scene origin if no model)
    if model_object:
        look_at_constraint = camera_object.constraints.new(type='TRACK_TO')
        look_at_constraint.target = model_object
        look_at_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        look_at_constraint.up_axis = 'UP_Y'
    else:
        # If no model, look at scene origin (0,0,0) - default behavior
        pass # Camera is already roughly looking at origin in default setup

    # Lighting setup (simple sun light)
    light_data = bpy.data.lights.new(name="Sun", type='SUN')
    light_object = bpy.data.objects.new("Sun", light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (5, 5, 5) # Position the light
    light_object.data.energy = 2 # Adjust light intensity

    # World background to white (optional, for cleaner look)
    bpy.data.worlds['World'].use_nodes = True
    bg_tree = bpy.data.worlds['World'].node_tree
    bg_node = bg_tree.nodes['Background']
    bg_node.inputs['Color'].default_value = (1, 1, 1, 1) # White background

    return camera_object

def get_model_object():
    """Attempts to find the main model object in the scene (assuming it's a mesh).
       Returns None if no mesh object is found, or if there are multiple and unclear which is the main one."""
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if not mesh_objects:
        return None
    elif len(mesh_objects) == 1:
        return mesh_objects[0]
    else:
        print("Warning: Multiple mesh objects found in the scene. Attempting to use the first one as the model. You might need to adjust the script if this is incorrect.")
        return mesh_objects[0] # Just return the first one as a simple approach


def render_angles(glb_filepath, output_dir, num_angles=36):
    """Renders images from different angles of the GLB model."""

    clear_scene()
    import_glb(glb_filepath)

    model_object = get_model_object()
    camera_object = setup_camera_and_lighting(model_object)

    if not model_object:
        print("Warning: No model object found after importing GLB. Rendering scene from angles without a focused model.")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    bpy.context.scene.render.image_settings.file_format = 'PNG' # Set output format to PNG

    # Calculate angles to rotate around the model
    angle_increment = 360.0 / num_angles
    for i in range(num_angles):
        angle_degrees = i * angle_increment
        angle_radians = math.radians(angle_degrees)

        # Rotate camera around Z axis (vertical axis) of the model's origin (or scene origin if no model)
        if model_object:
            pivot_point = model_object.location
        else:
            pivot_point = (0, 0, 0) # Scene origin

        # Calculate camera position in a circle around the pivot point
        distance_from_pivot = 3.0 # Adjust this distance as needed
        camera_x = pivot_point[0] + distance_from_pivot * math.cos(angle_radians)
        camera_y = pivot_point[1] + distance_from_pivot * math.sin(angle_radians)
        camera_z = camera_object.location[2] # Keep the same Z height for now


        camera_object.location = (camera_x, camera_y, camera_z)

        # Optionally, you can also vary the vertical angle (elevation) for more diverse views
        # For example, vary camera_z slightly based on i or some other pattern.
        # camera_z = 2 + 0.5 * math.sin(math.radians(i * (360.0 / num_angles))) # Example vertical variation


        # Update filename and output path
        output_filename = f"model_angle_{i:03d}.png"
        output_filepath = os.path.join(output_dir, output_filename)
        bpy.context.scene.render.filepath = output_filepath

        # Render the scene
        bpy.ops.render.render(write_still=True)
        print(f"Rendered image {i+1}/{num_angles}: {output_filename}")

    print(f"Rendering complete. Images saved to: {output_dir}")

if __name__ == '__main__':
    # --- HARDCODED PATHS AND SETTINGS ---
    glb_filepath = "/Users/tresmith/Documents/chegbot3000/glb3.glb"  # <--- MODIFY THIS TO YOUR GLB FILE PATH
    output_dir = "/Users/tresmith/Documents/chegbot3000/outputs"    # <--- MODIFY THIS TO YOUR OUTPUT DIRECTORY
    num_angles = 100                                                   # <--- MODIFY THIS TO DESIRED NUMBER OF ANGLES
    # ------------------------------------

    if not os.path.exists(glb_filepath):
        print(f"Error: GLB file not found at: {glb_filepath}")
    else:
        render_angles(glb_filepath, output_dir, num_angles)