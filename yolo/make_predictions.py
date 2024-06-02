import os
import shutil

def get_predictions(img_path):
    os.chdir("yolo")
    try:
        shutil.copy("get_predictions.py", "yolov7/get_predictions.py")
    except:
        pass

    try:
        shutil.copy('../' + img_path, "test.jpg")
    except:
        pass

    os.system("python yolov7/get_predictions.py")

    with open("predictions.txt") as file:
        output = [list(map(float, i.split())) for i in file.readlines()]

    os.remove("test.jpg")
    os.chdir("../")
    return output
