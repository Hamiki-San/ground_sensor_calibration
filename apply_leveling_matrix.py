import numpy as np
import open3d as o3d
import os

# --- CONFIGURATION ---

# Absolute path to your input root folder
PCD_ROOT_FOLDER = r"C:\Users\Hazimi\OneDrive\CEEM222 MEC698 Internship\ground_calibration\data\Sample"

# Final rotation matrix (replace with your calibration matrix)
FINAL_ROTATION_MATRIX = np.array([
    [1.0000, 0.0000, 0.0000],
    [0.0000, 0.95372, 0.300706],
    [0.0000, -0.300706, 0.95372]
])

# Output folder INSIDE your PCD_ROOT_FOLDER
OUTPUT_FOLDER = os.path.join(PCD_ROOT_FOLDER, "leveled_data")

# --- FUNCTIONS ---

def process_pcd_file(pcd_path, output_dir, rotation_matrix):
    """
    Loads a PCD file, finds the lowest point, applies a rotation, and saves the result.
    """
    try:
        pcd = o3d.io.read_point_cloud(pcd_path)
        points = np.asarray(pcd.points)

        if points.size == 0:
            print(f"⚠️ Empty point cloud: {pcd_path}")
            return

        # 1. Find the lowest point (pivot for rotation)
        lowest_point_idx = np.argmin(points[:, 2])
        lowest_point = points[lowest_point_idx, :]

        # 2. Translate so lowest point is at the origin
        translated_points = points - lowest_point

        # 3. Rotate
        rotated_points = translated_points @ rotation_matrix.T

        # 4. Translate back
        leveled_points = rotated_points + lowest_point

        # 5. Build new cloud
        leveled_pcd = o3d.geometry.PointCloud()
        leveled_pcd.points = o3d.utility.Vector3dVector(leveled_points)

        # 6. Save
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
