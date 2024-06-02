import cv2 as cv
import numpy as np
import glob


for img_name in glob.glob("data/*"):
    img = cv.imread(img_name)
    show_size = (360, 480)
    img = cv.resize(img, show_size)

    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)


    colorLow = np.array([20,55,30])
    colorHigh = np.array([120,97,218])
    mask = cv.inRange(hsv_img, colorLow, colorHigh)

    kernal = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernal)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernal)

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(img, contours, -1, (0,255,0), 3)

    cv.imshow(None, img)
    cv.waitKey(5000)