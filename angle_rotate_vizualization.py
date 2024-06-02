import cv2 as cv
import numpy as np
import json
import sys

def affine_transform(x, y, mat, bias=np.array((0, 0))):
    return mat @ np.array((x, y)) + bias


def Oxy_tranform(x, y, e1, e2, bias=np.array((0, 0))):
    s = np.linalg.inv(np.array((e1, e2)))
    return np.array(s) @ np.array((x, y)) + bias


def Oxy_tranform_back(x, y, e1, e2, bias=np.array((0, 0))):
    s = np.array((e1, e2))
    return s @ np.array((x, y)) + bias



def transform(x, y):
    return int(x), int(y) 



flag = True
points = json.load(open("base_points.json"))["hexagon"]["coordinates"]

t_points = [(553, 678), (489, 717), (419, 681), (419, 605), (486, 562), (551, 602)]

if not flag:
    phi = 3.14 * np.random.random() / 6
    transform_mat = np.array(((np.cos(phi), -np.sin(phi)), (np.sin(phi), np.cos(phi))))

eps = 0.1
alpha = 3.14

for i in range(len(points)):
    for j in range(len(points)):
        if (i == j):
            continue

        
        x0, y0 = points[i]
        x1, y1 = points[j]
        
        e1 = np.array((x1 - x0, y1 - y0))
        e2 = np.array((y1 - y0, x0 - x1))
        bias = np.array((x0, y0))


        for k in range(len(points)):
            for l in range(len(points)):
                if (k == l):
                    continue
                
                frame = np.zeros((1000, 1000, 3))

                if not flag:
                    x0_t, y0_t = points[k]
                    x1_t, y1_t = points[l]

                    x0_t, y0_t = affine_transform(x0_t, y0_t, transform_mat)
                    x1_t, y1_t = affine_transform(x1_t, y1_t, transform_mat)
                else:
                    x0_t, y0_t = t_points[k]
                    x1_t, y1_t = t_points[l]

                e1_t = np.array((x1_t - x0_t, y1_t - y0_t))
                e2_t = np.array((y1_t - y0_t, x0_t - x1_t))
                bias_t = np.array((x0_t, y0_t))
                
                norm = (np.linalg.norm(e1) / np.linalg.norm(e1_t))

                frame = cv.line(img=frame, pt1=transform(x0_t, y0_t), pt2=transform(x1_t, y1_t), color=(0, 0, 255), thickness=4)
                frame = cv.line(img=frame, pt1=transform(x0_t, y0_t), pt2=transform(*(np.array((x0_t, y0_t)) + e2_t)), color=(255, 0, 0), thickness=4)

                points_t = list()
                for p_t in range(len(points)):
                    if not flag:
                        points_t.append(affine_transform(*points[p_t], mat=transform_mat))
                    else:
                        points_t.append(t_points[p_t])

                    if p_t == k:
                        frame = cv.circle(img=frame, center=transform(*points_t[-1]), radius=5, color=(255, 0, 255), thickness=-1)
                    elif p_t == l:
                        frame = cv.circle(img=frame, center=transform(*points_t[-1]), radius=5, color=(0, 0, 255), thickness=-1)
                    else:
                        frame = cv.circle(img=frame, center=transform(*points_t[-1]), radius=5, color=(255, 255, 255), thickness=-1)
                    frame = cv.putText(img=frame, text=str(p_t), org=transform(*points_t[-1] - np.array((0.2, 0.2))), fontFace=0, fontScale=0.7, color=(255, 255, 255), thickness=1)
                
                new_points = list()
                for p in range(len(points)):
                    new_x_y = Oxy_tranform(*(np.array(list(points[p])) - bias), e1, e2)
                    new_x_y_t = Oxy_tranform_back(*new_x_y, e1_t, e2_t, np.array((x0_t, y0_t)))
                    new_points.append(new_x_y_t)
                    frame = cv.circle(img=frame, center=transform(*new_x_y_t), radius=3, color=(0, 255, 0), thickness=-1)
                    frame = cv.putText(img=frame, text=str(p), org=transform(*new_x_y_t + np.array((0.1, 0.1))), fontFace=0, fontScale=0.5, color=(0, 255, 0), thickness=1)

                fl = False
                if np.all(norm * np.abs(np.sort(np.array(points_t), axis=0) - np.sort(np.array(new_points), axis=0)) < eps):
                    rot_matrix = (np.array((e1_t, e2_t)) @ np.linalg.inv(np.array((e1, e2))) * (np.linalg.norm(e1) / np.linalg.norm(e1_t)))
                    if abs(np.arctan(rot_matrix[1][0] / rot_matrix[0][0])) < alpha:
                        alpha = np.arctan(rot_matrix[1][0] / rot_matrix[0][0])
                    fl = True

                if fl:
                    frame = cv.putText(img=frame, text=f"alpha={round(alpha, 2)} rad", org=(190, 100), fontFace=0, fontScale=0.5, color=(255, 255, 255), thickness=1)
                cv.imshow(None, cv.resize(frame, (500, 500)))
                
                if cv.waitKey() == ord('q'):
                    sys.exit(0)
