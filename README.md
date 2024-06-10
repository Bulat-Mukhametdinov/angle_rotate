# Bolt Rotation Angle Detector

This project determines the angle of rotation of bolts by analyzing images.

## Installation

Only for windows
1. `git clone https://github.com/Bulat-Mukhametdinov/angle_rotate.git`
2. `cd angle_rotate.git`
3. Run `init.bat` to install the required dependencies.
4. Download the YOLO weights from [Google Drive](https://drive.google.com/drive/folders/13xgcezmCsH3BguBzeVez_sCkcvsUSOxx?usp=sharing) and clone them to the `yolo/` folder.

## Usage

1. If you want to use your own images place them in the `data/` folder
2. Run the program using the command `python main.py`.
3. Use the "next" and "prev" buttons to navigate through the images.
4. Click the "choose" button to select the image you want to analyze.
5. The program will run the YOLO keypoints detection model to find the bolt on the image.
6. If the keypoints are found correctly, the program will determine the rotation angle.
7. If the keypoints cannot be found, the program will print the message "impossible to determine angle" on the window.
8. Use 'q' to exit the program
