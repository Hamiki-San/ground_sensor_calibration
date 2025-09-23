import open3d as o3d
import numpy as np
import os
from math import radians

# --- CONFIGURATION ---
# Path to the specific subfolder containing the point cloud data
PCD_FOLDER = r'C:\Users\Hazimi\OneDrive\CEEM222 MEC698 Internship\ground_calibration\data\0,0,0'

# Global variables for the current rotation angles
current_roll = 0.0
current_pitch = 0.0
current_yaw = 0.0

def update_point_cloud(vis, original_pcd):
    """
    Updates the point cloud in the visualizer based on the current global angles.
    """
    global current_roll, current_pitch, current_yaw

    # Create the rotation matrix
    roll_rad = radians(current_roll)
    pitch_rad = radians(current_pitch)
    yaw_rad = radians(current_yaw)

    rotation_matrix = original_pcd.get_rotation_matrix_from_xyz((roll_rad, pitch_rad, yaw_rad))

    # Apply the rotation
    leveled_pcd = original_pcd.transform(np.vstack([np.hstack([rotation_matrix, np.zeros((3, 1))]),
                                                       [0, 0, 0, 1]]))

    # Update the geometry in the visualizer
    vis.update_geometry(leveled_pcd)
    vis.update_renderer()

    # Print the rotation matrix to the console
    print(f"\n--- Current Rotation Matrix for Roll: {current_roll}, Pitch: {current_pitch}, Yaw: {current_yaw} ---")
    print(np.array2string(rotation_matrix, formatter={'float_kind':lambda x: "%.4f" % x}))
    print("--------------------------------------------------\n")

def key_press_callback(vis, action, mods):
    """
    Callback function to handle key presses for rotation.
    """
    global current_roll, current_pitch, current_yaw

    if action == 1: # Key press
        if vis.get_key_state(ord('W')):
            current_pitch += 1.0
        if vis.get_key_state(ord('S')):
            current_pitch -= 1.0
        if vis.get_key_state(ord('A')):
            current_roll += 1.0
        if vis.get_key_state(ord('D')):
            current_roll -= 1.0
        if vis.get_key_state(ord('Q')):
            current_yaw -= 1.0
        if vis.get_key_state(ord('E')):
            current_yaw += 1.0
        
        # Update the visualizer with the new angles
        update_point_cloud(vis, pcd_original)
    return False

# --- MAIN SCRIPT EXECUTION ---
print("Starting Open3D leveling tool...")
print("Instructions:")
print(" - Press 'W' to increase Pitch")
print(" - Press 'S' to decrease Pitch")
print(" - Press 'A' to increase Roll")
print(" - Press 'D' to decrease Roll")
print(" - Press 'Q' to decrease Yaw")
print(" - Press 'E' to increase Yaw")
print(" - Press 'Esc' to exit the visualizer")

# Check if the folder exists
if not os.path.isdir(PCD_FOLDER):
    print(f"\nError: The directory '{PCD_FOLDER}' was not found.")
else:
    pcd_files = sorted([f for f in os.listdir(PCD_FOLDER) if f.endswith('.pcd')])

    if not pcd_files:
        print("\n  - No PCD files found in this folder. Exiting.")
    else:
        file_path = os.path.join(PCD_FOLDER, pcd_files[0])
        print(f"\nProcessing file: '{file_path}'")
        
        pcd_original = o3d.io.read_point_cloud(file_path)
        
        vis = o3d.visualization.VisualizerWithKeyCallback()
        vis.create_window(window_name='Open3D Leveling Tool', width=800, height=700)
        
        # Add the initial point cloud
        vis.add_geometry(pcd_original)
        
        # Set camera position for better view
        ctr = vis.get_view_control()
        ctr.set_lookat([0, 0, 0])
        ctr.set_up([0, 0, 1])
        ctr.set_front([0, -1, 0])

        # Register key press callback
        vis.register_key_callback(87, key_press_callback) # W
        vis.register_key_callback(83, key_press_callback) # S
        vis.register_key_callback(65, key_press_callback) # A
        vis.register_key_callback(68, key_press_callback) # D
        vis.register_key_callback(81, key_press_callback) # Q
        vis.register_key_callback(69, key_press_callback) # E
        
        # Start the visualizer
        vis.run()
        vis.destroy_window()
