import math
from utils import *

def get_angle(points):
    cx, cy = get_center(points)
    cos_alpha = -1
    pos_x = 0

    for p in points:
        x, y = p
        radius = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5

        cur_cos_alpha = min(1, ((cy - y) * radius) / (radius ** 2))
        if cur_cos_alpha > cos_alpha:
            cos_alpha = cur_cos_alpha
            pos_x = x

    alpha = math.acos(cos_alpha)

    if pos_x < cx:
        alpha = -alpha
    
    return alpha, (int(cx), int(cy))