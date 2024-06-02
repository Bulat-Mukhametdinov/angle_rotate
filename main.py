from src.constants import *
from src.utils import *
from src.get_angle import get_angle
from yolo.make_predictions import get_predictions
import cv2 as cv
import numpy as np
import math
import glob
import sys


class Button:
    def __init__(self, x, y, text, font_scale):
        self.x = x
        self.y = y
        self.font_scale = font_scale
        self.text = text

        text_size, *_ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, font_scale, 2)
        self.w = text_size[0] + 20
        self.h = text_size[1] + 10

        self.rendered_button = np.ones((self.h, self.w, 3), dtype=np.uint8) * 255
        self.rendered_button = cv.rectangle(self.rendered_button, (0, 0), (self.w - 1, self.h - 1), color=(0, 0, 0), thickness=2)
        self.rendered_button = cv.putText(self.rendered_button, text, (10, self.h - 5), cv.FONT_HERSHEY_SIMPLEX, font_scale, color=(0, 0, 0), thickness=2)

    def check4click(self, x, y):
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            return True
        else:
            return False


class CoordinateStorage:
    def __init__(self):
        self.point = [None, None]
    
    def click_event(self, event, x, y, flags, params):
        if event == cv.EVENT_LBUTTONDOWN:
            self.point[0] = x
            self.point[1] = y
    
    def empty_points(self):
        self.point = [None, None]


def render_window(images, mode, buttons, dots=None, rects=None, angle=None):
    window = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH, CHANNELS), dtype=np.uint8) * 255
    for b in buttons:
        window[b.y: b.y + b.h, b.x: b.x + b.w] = b.rendered_button
    
    if dots is not None:
        for dot in dots:
            cv.circle(images, dot, 4, (0, 0, 255), -1)
    if rects is not None:
        cv.putText(window, f"{len(rects)} objects", (10, 300), 0, 2, (0, 0, 0), 2)
        for rect in rects:
            cv.rectangle(images, rect[0], rect[1], (0, 255, 0), 2)

    if angle == 404:
        cv.putText(window, f"imposible to", (900, 300), 0, 1, (0, 0, 0), 2)
        cv.putText(window, f"determine angle", (900, 330), 0, 1, (0, 0, 0), 2)
    elif angle is not None:
        cv.putText(window, f"{angle} rad", (900, 300), 0, 1, (0, 0, 0), 1)
    
    if mode == 1 or mode == 2:
        h, w, *_ = images.shape
        new_size = int(CROP_SIZE * 1.5)
        img = cv.resize(images, (int(new_size / (h / w)), new_size))
        h, w, *_ = img.shape
        window[10:10 + h, (WINDOW_WIDTH - w) // 2: (WINDOW_WIDTH - w) // 2 + w] = img
    else:
        left_img, right_img = images
        window[LEFT_yOFFSET:LEFT_yOFFSET + CROP_SIZE, LEFT_xOFFSET:LEFT_xOFFSET + CROP_SIZE] = left_img
        window[RIGHT_yOFFSET:RIGHT_yOFFSET + CROP_SIZE, RIGHT_xOFFSET:RIGHT_xOFFSET + CROP_SIZE] = right_img
    
    return window


def main():
    raw_coords = list()
    coords = list()
    pressedDone = False

    image_paths = "data/"
    samples = glob.glob(image_paths + "*.png") + glob.glob(image_paths + "*.jpg") 

    storage = CoordinateStorage()

    main_buttons = [Button(400, 520, "prev", 2),
                    Button(620, 520, "next", 2),
                    Button(800, 520, "choose", 2)]

    angle = None
    img_id = 0
    mode = 1
    rects = None
    pts = None

    while True:

        if mode == 1:
            img = cv.imread(samples[img_id])
            buttons = main_buttons
        elif mode == 2:
            buttons = [Button(500, 520, "back", 2),]
        window = render_window(img, mode, buttons, pts, rects, angle)
        cv.imshow(WINDOW_NAME, window)
        

        cv.setMouseCallback(WINDOW_NAME, storage.click_event)
        if storage.point[0] is not None:
            x, y = storage.point
        else:
            x, y = -1, -1

        
        if mode == 1:
            if buttons[0].check4click(x, y):
                img_id = max(0, img_id - 1)
                storage.empty_points()
            elif buttons[1].check4click(x, y):
                img_id = min(len(samples) - 1, img_id + 1)
                storage.empty_points()
            elif buttons[2].check4click(x, y):
                mode = 2
                storage.empty_points()
                continue
        
        if mode ==2:
            if buttons[0].check4click(x, y):
                rects = None
                pts = None
                angle = None
                mode = 1
                storage.empty_points()

        if cv.waitKey(1) == ord('q'):
            break

        if mode == 2 and rects is None:
            rects = []
            pts = []
            for label in get_predictions(samples[img_id]):
                cx, cy, w, h, conf, *kpts = label
                height, width, _ = img.shape
                cx *= width
                cy *= height
                w *= width
                h *= height

                rects.append(((int(cx - w / 2), int(cy - h / 2)), (int(cx + w / 2), int(cy + h / 2))))
                points = list()
                for i in range(0, len(kpts), 3):
                    pts.append((int(kpts[i] * width), int(kpts[i + 1] * height)))
                    points.append(pts[-1])
                
                if len(points) == 6 and (angle == 404 or angle is None):
                    angle = get_angle(points, "hexagon")
                else:
                    angle = 404

if __name__ == "__main__":
    main()