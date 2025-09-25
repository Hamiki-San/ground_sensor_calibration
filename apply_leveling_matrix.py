import numpy as np
import open3d as o3d
import os

# --- CONFIGURATION ---

# Absolute path to your input root folder
PCD_ROOT_FOLDER = r"C:\Users\Hazimi\OneDrive\CEEM222 6M MEC698 Internship\ground_calibration\data"

# Final rotation matrix (replace with your calibration matrix)
FINAL_ROTATION_MATRIX = np.array([
    [1.0000, 0.0000, 0.0000],
    [0.0000, 0.95372, 0.300706],
    [0.0000, -0.300706, 0.95372]
])

# Output folder INSIDE your PCD_ROOT_FOLDER
OUTPUT_FOLDER = os.path.join(PCD_ROOT_FOLDER, "leveled_data_ii")

# --- FUNCTIONS ---

def process_pcd_file(pcd_path, output_dir, rotation_matrix):
    """
    Loads a PCD file, applies a rotation around the global origin (0,0,0),
    and saves the result.
    """
    try:
        pcd = o3d.io.read_point_cloud(pcd_path)
        points = np.asarray(pcd.points)

        if points.size == 0:
            print(f"⚠️ Empty point cloud: {pcd_path}")
            return

        # ✅ Rotate directly around the global origin (0,0,0)
        rotated_points = points @ rotation_matrix.T

        # Build new cloud
        leveled_pcd = o3d.geometry.PointCloud()
        leveled_pcd.points = o3d.utility.Vector3dVector(rotated_points)

        # Save
        file_name = os.path.basename(pcd_path)
        output_path = os.path.join(output_dir, file_name)
        o3d.io.write_point_cloud(output_path, leveled_pcd)

        print(f"✅ Saved: {output_path}")

    except Exception as e:
        print(f"❌ Failed {pcd_path}: {e}")

# --- MAIN SCRIPT ---

if __name__ == "__main__":
    print("Starting batch leveling process...")
    print("-" * 40)

    # Debug info
    print("Script location:", os.path.dirname(os.path.abspath(__file__)))
    print("Current working dir:", os.getcwd())
    print("PCD root:", PCD_ROOT_FOLDER)
    print("Output folder:", OUTPUT_FOLDER)

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Process only top-level files
    for file in os.listdir(PCD_ROOT_FOLDER):
        if file.lower().endswith(".pcd"):
            file_path = os.path.join(PCD_ROOT_FOLDER, file)
            print(f"Processing: {file_path}")
            process_pcd_file(file_path, OUTPUT_FOLDER, FINAL_ROTATION_MATRIX)

    print("-" * 40)
    print("Batch leveling complete.")
