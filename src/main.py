from src.constants import *
from src.utils import *
from src.get_angle import get_angle
import cv2 as cv
import numpy as np
import math
import glob


def render_window(left_img, right_img, angle=None, dots=None, pressedDone=False):
    window = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH, CHANNELS), dtype=np.uint8) * 255
    window[LEFT_yOFFSET:LEFT_yOFFSET + CROP_SIZE, LEFT_xOFFSET:LEFT_xOFFSET + CROP_SIZE] = left_img
    window[RIGHT_yOFFSET:RIGHT_yOFFSET + CROP_SIZE, RIGHT_xOFFSET:RIGHT_xOFFSET + CROP_SIZE] = right_img
    
    b1ul, b1lr = (620, 520), (800, 590)  # button1 upper left, lower right corner
    text1Pos = (635, 575)                # text1 lower left corner
    b2ul, b2lr = (400, 520), (580, 590)
    text2Pos = (415, 575)
    if not pressedDone:
        text1 = "Done"
        text2 = "Redo"
    else:
        text1 = "Stop"
        text2 = "Flip"

    # button1 
    cv.rectangle(window, b1ul, b1lr, 0, 2)
    cv.putText(window, text1, text1Pos, 0, 2, 0, 2)
    # button2
    cv.rectangle(window, b2ul, b2lr, 0, 2)
    cv.putText(window, text2, text2Pos, 0, 2, 0, 2)

    if angle is None:
        angle = 0
    draw_arrow(window, -angle)
    
    if dots is not None:
        for dot in dots:
            cv.circle(window, dot, 4, (0, 0, 255), -1)
    
    return window

class CoordinateStorage:
    def __init__(self):
        self.point = [None, None]
    
    def click_event(self, event, x, y, flags, params):
        if event == cv.EVENT_LBUTTONDOWN:
            self.point[0] = x
            self.point[1] = y



def main():
    raw_coords = list()
    coords = list()
    pressedDone = False

    sample = cv.imread("test.jpg")
    h, w, *oth = sample.shape


    storage = CoordinateStorage()
    angle = 0
    rotation = 1
    dir = 1
    img_id = 0

    while True:

        if pressedDone:
            for i in range(len(raw_coords)):
                coords[i] = pointRotate(raw_coords[i], angle / 180 * math.pi, (w // 2, h // 2))
            angle_rotate, center = get_angle(coords, "hexagon")
            angle_rotate = angle_rotate / math.pi * 180
        else:
            angle_rotate, center = 0, (w // 2, h // 2)

        leftImg = rotateImg(sample, (w // 2, h // 2), angle)
        rightImg = rotateImg(leftImg, center, angle_rotate)

        leftImg = cropImg(leftImg, (w // 2, h // 2), CROP_SIZE)
        rightImg = cropImg(rightImg, center, CROP_SIZE)
        dots = list()
        for p in coords:
            px, py = p
            dots.append((px + LEFT_xOFFSET - (w - CROP_SIZE) // 2, py + LEFT_yOFFSET - (h - CROP_SIZE) // 2))
        window = render_window(leftImg, rightImg, angle_rotate, dots, pressedDone)
        cv.imshow(WINDOW_NAME, window)
        
        cv.setMouseCallback(WINDOW_NAME, storage.click_event)
        if storage.point[0] is not None:
            x, y = storage.point
            if LEFT_xOFFSET <= x < LEFT_xOFFSET + CROP_SIZE and LEFT_yOFFSET <= y < LEFT_yOFFSET + CROP_SIZE:
                if not pressedDone:
                    raw_coords.append((x - LEFT_xOFFSET + (w - CROP_SIZE) // 2, y - LEFT_yOFFSET + (h - CROP_SIZE) // 2))
                    coords.append((x - LEFT_xOFFSET + (w - CROP_SIZE) // 2, y - LEFT_yOFFSET + (h - CROP_SIZE) // 2))
            elif 620 <= x <= 800 and 520 <= y <= 590:
                if pressedDone:
                    rotation = not rotation
                else:
                    if len(coords):
                        pressedDone = not pressedDone
            elif 400 <= x <= 580 and 520 <= y <= 590:
                if pressedDone:
                    dir *= -1
                    rotation = 1
                else:
                    raw_coords.clear()
                    coords.clear()
            storage.point = [None, None]

        if cv.waitKey(10) == ord('q'):
            break
        if pressedDone:
            angle += 1 * dir * rotation
            if angle >= 360:
                angle -= 360
            elif angle <= -360:
                angle += 360


if __name__ == "__main__":
    main()