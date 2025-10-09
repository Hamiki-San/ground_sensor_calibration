# My Jupyter Notebook Project

This repository contains a Jupyter Notebook for image calibration involving rotation and translation.

## Contents
- `notebook.ipynb` – main notebook
- `data/` – dataset folder (if applicable)

## How to run
1. Clone the repo:
   ```bash
   git clone https://github.com/username/repo-name.git


## WORKING PROCEDURE FOR THE CALIBRATION PROCESS
1. Place the marker on the plane ground marking interception so can be detected from the pcd image view. Marker can be anything with sharp corner (printed marker box) or else, a cone will works too with lower accuracy.
2. Take a snapshot of the marker at fews known position, as sample to first verified the calibration accuracy after being rotated.
1. Rotate the PCD frame about its datum's x-axis so the ground was level using `1. Rotation about x-axis of original datum (0, 0, 0)` cell.
2. Take the rotation matrix and assign into the calibration matrix of [R,0|t,1].
3. Load the leveled data to pinpoint teh coordinate of teh desired new datum, take note of the coordinate and replace the value of translation vector in [R,0|t,1] matrix.
4. Run `Applying whole calibration matrix` with noted value of the calibration matrix to the folder of uncalibrated (both rotated and translated) files.
5. (OPTIONAL) Load scripts of `Differences between uncalibrated and calibrated files/folder viewer` to see the differences of coordinates, both new and old. This viewer is also can be use to verified the distance between marker of known real setup distance.

### Consideration took from the calibration method planning.
1. The pcd view must not be subjected to yaw and rolling as the calibration of rotation wrt to pitch angle is being done in this calibration.
2. Selection of new point from sharp corner is the only manual process that involve in calibration, hence this process has high probability to prone for error. 