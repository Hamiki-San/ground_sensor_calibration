import numpy as np
import open3d as o3d
import os

# --- CONFIGURATION ---

# The full path to the folder containing all the original PCD files.
PCD_ROOT_FOLDER = r"C:\Users\Hazimi\OneDrive\CEEM222 6M MEC698 Internship\ground_calibration\data"

# Final calibration matrix (a combined 4x4 rotation and translation).
# THIS IS YOUR FINAL MATRIX FROM THE CALIBRATION STEP.
# Paste the 4x4 matrix you provided here.
FINAL_CALIBRATION_MATRIX = np.array([
    [ 1.        ,  0.        ,  0.        ,  0.05546083],
    [ 0.        ,  0.95372   ,  0.300706  , -2.369946  ],
    [ 0.        , -0.300706  ,  0.95372   ,  0.5661217 ],
    [ 0.        ,  0.        ,  0.        ,  1.        ]
])

# The name of the output folder that will be created
OUTPUT_FOLDER_NAME = "calibrated_data"
OUTPUT_FOLDER_PATH = os.path.join(PCD_ROOT_FOLDER, OUTPUT_FOLDER_NAME)

# --- FUNCTIONS ---

def apply_calibration_to_pcd(pcd_path, output_dir, calibration_matrix):
    """
    Loads a PCD file, applies a single, pre-calculated calibration matrix,
    and saves the result to the output directory.
    """
    try:
        # Load the point cloud
        pcd = o3d.io.read_point_cloud(pcd_path)
        
        if len(pcd.points) == 0:
            print(f"⚠️ Empty point cloud: {pcd_path}")
            return

        # Apply the transformation matrix directly to the point cloud
        # This is the key step that applies your entire calibration.
        pcd.transform(calibration_matrix)
        
        # Save the new point cloud
        file_name = os.path.basename(pcd_path)
        output_path = os.path.join(output_dir, file_name)
        o3d.io.write_point_cloud(output_path, pcd)

        print(f"✅ Saved: {output_path}")

    except Exception as e:
        print(f"❌ Failed to process {pcd_path}: {e}")
        print(f"Error details: {e}")

# --- MAIN SCRIPT ---

if __name__ == "__main__":
    print("Starting batch calibration process...")
    print("-" * 40)

    print(f"Processing files in: {PCD_ROOT_FOLDER}")
    print(f"Output folder path: {OUTPUT_FOLDER_PATH}")
    
    # Ensure output folder exists
    try:
        os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)
        print(f"✅ Output folder verified/created successfully at '{OUTPUT_FOLDER_PATH}'.")
    except PermissionError:
        print(f"❌ Error: Permission denied. The script cannot create the folder at '{OUTPUT_FOLDER_PATH}'.")
        print("Please run your terminal as an administrator.")
        exit()

    # Process all PCD files in the root folder
    found_files = False
    for file in os.listdir(PCD_ROOT_FOLDER):
        file_path = os.path.join(PCD_ROOT_FOLDER, file)
        
        if os.path.isfile(file_path) and file.lower().endswith(".pcd"):
            found_files = True
            print(f"Processing: {file_path}")
            apply_calibration_to_pcd(file_path, OUTPUT_FOLDER_PATH, FINAL_CALIBRATION_MATRIX)

    if not found_files:
        print("⚠️ No .pcd files found in the specified root folder. Please check your path.")

    print("-" * 40)
    print("Batch calibration complete.")
