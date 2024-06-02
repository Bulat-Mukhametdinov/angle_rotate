import numpy as np
import json
import math
from src.utils import get_center

def get_angle(points, connection_type):
    cx, cy = get_center(points)

    base_pts = json.load(open("src/base_points.json"))[connection_type]["coordinates"]

    eps = 0.1
    alpha = math.pi

    for i in range(len(base_pts)):
        for j in range(len(base_pts)):
            if (i == j):
                continue

            x0, y0 = base_pts[i]
            x1, y1 = base_pts[j]
            
            e1 = np.array((x1 - x0, y1 - y0))
            e2 = np.array((y1 - y0, x0 - x1))
            bias = np.array((x0, y0))


            for k in range(len(points)):
                for l in range(len(points)):
                    if (k == l):
                        continue
                    
                    x0_t, y0_t = points[k]
                    x1_t, y1_t = points[l]

                    e1_t = np.array((x1_t - x0_t, y1_t - y0_t))
                    e2_t = np.array((y1_t - y0_t, x0_t - x1_t))
                    bias_t = np.array((x0_t, y0_t))
                    
                    norm = (np.linalg.norm(e1) / np.linalg.norm(e1_t))
                    
                    base_pts_in_new_basis = list()
                    for p in range(len(base_pts)):
                        new_x_y = np.linalg.inv(np.array((e1, e2))) @ (np.array(base_pts[p]) - bias)
                        new_x_y = np.array((e1_t, e2_t)) @ new_x_y + bias_t
                        base_pts_in_new_basis.append(new_x_y)

                    if np.all(norm * np.abs(np.sort(np.array(points), axis=0) - np.sort(np.array(base_pts_in_new_basis), axis=0)) < eps):
                        rot_matrix = (np.array((e1_t, e2_t)) @ np.linalg.inv(np.array((e1, e2))) * norm)
                        
                        if rot_matrix[0, 0] == 0:
                            return -math.pi / 2
                        else:
                            possible_alpha = np.arctan(rot_matrix[0, 1] / rot_matrix[0, 0])
                        if abs(possible_alpha) < alpha:
                            return -possible_alpha
    
    return 404