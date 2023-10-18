# Imports
import bpy
import csv
import os
import math

# Clear all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Path to CSV
cd = os.path.dirname(bpy.data.filepath)
csv_path = os.path.join(cd, 'Plot_Data', '2D_Isotropic_Beam_6.51E-06_3000' + '.csv')

# Open the CSV file and read the data into list
csv_data = []
max_displacement = 0
with open(csv_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x = float(row[0])
        y = float(row[1])
        displacement_x = float(row[2])
        displacement_y = float(row[3])
        if math.sqrt(displacement_x**2 + displacement_y**2) > max_displacement: max_displacement = math.sqrt(displacement_x**2 + displacement_y**2)
        csv_data.append([x, y, displacement_x, displacement_y])

# Animation parameters
duration = 3  # Animation duration in seconds
frame_rate = 24  # Frame rate (frames per second)
total_frames = duration * frame_rate

# Create spheres for each data point and animate them
for data in csv_data:
    x, y, displacement_x, displacement_y = data
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(x, y, 0))
    sphere = bpy.context.object

    # Create a material for the sphere
    material = bpy.data.materials.new(name=f"ColorMaterial_{x}_{y}")
    sphere.data.materials.append(material)

    # Animate sphere movement
    for frame in range(total_frames):
        x_new = x + displacement_x * (frame / total_frames)
        y_new = y + displacement_y * (frame / total_frames)
        sphere.location = (x_new, y_new, 0)

        # Calculate the normalized value for this frame based on displacement magnitude
        magnitude = math.sqrt((displacement_x * (frame / total_frames))**2 + (displacement_y * (frame / total_frames))**2)
        normalized_value = min(1.0, magnitude / max_displacement)
        r = normalized_value
        g = 1.0 - normalized_value
        b = 0.0
        a = 1

        # Update the material's diffuse color for each frame
        material.diffuse_color = (r, g, b, a)

        # Set keyframes to animate location and color
        sphere.keyframe_insert(data_path="location", frame=frame)
        material.keyframe_insert(data_path="diffuse_color", frame=frame)

# Animation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = total_frames
bpy.ops.screen.animation_play()