# Imports
import bpy
import csv
import os

# Clear all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


cd = os.path.dirname(bpy.data.filepath)
# Path to csv
csv_path = os.path.join(cd, 'Plot_Data', '2D_Isotropic_Beam_6.51E-06_3000' + '.csv')

# List for csv data
csv_data = []

# Open the CSV file and read the data into list
with open(csv_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        x = float(row[0])
        y = float(row[1])
        displacement_x = float(row[2])
        displacement_y = float(row[3])
        csv_data.append([x, y, displacement_x, displacement_y])

# Animation parameters
duration = 10  # Animation duration in seconds
frame_rate = 24  # Frame rate (frames per second)
total_frames = duration * frame_rate

# Create spheres for each data point and animate them
for data in csv_data:
    x, y, displacement_x, displacement_y = data
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(x, y, 0))
    sphere = bpy.context.object

    # Animate sphere movement
    for frame in range(total_frames):
        x_new = x + displacement_x * (frame / total_frames)
        y_new = y + displacement_y * (frame / total_frames)
        sphere.location = (x_new, y_new, 0)

        # Set keyframes to animate location
        sphere.keyframe_insert(data_path="location", frame=frame)

# Render settings (customize as needed)
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Render the animation
bpy.ops.render.render(animation=True)