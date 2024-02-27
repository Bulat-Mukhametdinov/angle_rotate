import cv2 as cv
from constants import *
import math

def draw_arrow(window, angle: float):
    
    # Draw point at center
    center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    color = 0
    
    img = cv.circle(window, center, 10, color, -1)

    # Draw angle change
    radius = 100
    axes = (radius, radius)
    startAngle = -90
    endAngle = startAngle + angle
    thickness = 10
    
    img = cv.ellipse(img, center, axes, 0, startAngle, endAngle, color, thickness)

    # Put text
    point = (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 120)
    text = f"{abs(round(angle, 2))} degrees"
    fontFace = 0

    img = cv.putText(img, text, point, fontFace, 1, 0)


    return img


def rotateImg(img, centerPoint: tuple, angle: float):
    h, w, *oth = img.shape

    M = cv.getRotationMatrix2D(centerPoint, angle, 1.0)
    rotated = cv.warpAffine(img, M, (w, h))

    return rotated


def cropImg(img, centerPoint: tuple, cropSize: int):
    y1, y2 = centerPoint[1] - cropSize // 2, centerPoint[1] + cropSize // 2
    x1, x2 = centerPoint[0] - cropSize // 2, centerPoint[0] + cropSize // 2
    return img[y1: y2, x1: x2]


def pointRotate(point, angle, center_point):
    x, y = point
    cx, cy = center_point
    vx, vy = x - cx, y - cy
    px = vx * math.cos(angle) + vy * math.sin(angle) + cx
    py = vy * math.cos(angle) - vx * math.sin(angle) + cy
    return (int(px), int(py))

def get_center(points):
    cx, cy = 0, 0
    for p in points:
        cx += p[0]
        cy += p[1]
    cx //= len(points)
    cy //= len(points)
    return (cx, cy)