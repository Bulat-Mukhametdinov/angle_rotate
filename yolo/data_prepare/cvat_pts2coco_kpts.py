import xml.etree.ElementTree as ET
import os
import sys
import shutil
import cv2


# labels_pth = "C:\\Users\\myx0j\\Downloads\\data\\annotations.xml"
# images_dir = "C:\\Users\\myx0j\\Downloads\\npu-bolt-DatasetNinja\\ds\\img\\"
labels_pth = "C:\\Users\\myx0j\\Downloads\\annotations\\annotations.xml"
images_dir = "C:\\Users\\myx0j\\Projects\\angle_rotate\\data\\"


dataset_dir = "dataset\\"

mode = "val\\"

# try:
#     os.mkdir(dataset_dir)
# except:
#     shutil.rmtree(dataset_dir)
#     os.mkdir(dataset_dir)

# os.mkdir(dataset_dir + "images\\")
# os.mkdir(dataset_dir + "labels\\")

os.mkdir(dataset_dir + "images\\" + mode)
os.mkdir(dataset_dir + "labels\\" + mode)


tree = ET.parse(labels_pth)
root = tree.getroot()

main_file = open(dataset_dir + mode[:-1] + '.txt', 'w')

for child in root:
    if child.tag == "image":
        img_name = child.attrib["name"]
        width = int(child.attrib["width"])
        height = int(child.attrib["height"])

        main_file.write(f"/images/{mode[:-1]}/{img_name}\n")

        img = cv2.imread(images_dir + img_name)

        cv2.imwrite(dataset_dir + "images\\" + mode + img_name, cv2.resize(img, (640, 640)))

        with open(dataset_dir + "labels\\" + mode + img_name[:-4] + '.txt', 'w') as file:
            for obj in child:
                if obj.attrib["label"] != 'bolt':
                    continue

                points = sorted(
                    tuple(
                        map(
                            lambda x: (
                                float(x.split(',')[0]) / width,
                                float(x.split(',')[1]) / height),
                            obj.attrib["points"].split(";")
                            )
                        )
                    )

                
                top_left_x = min([i[0] for i in points])
                top_left_y = min([i[1] for i in points])
                bottom_right_x = max([i[0] for i in points])
                bottom_right_y = max([i[1] for i in points])

                cx, cy = (top_left_x + bottom_right_x) / 2, (top_left_y + bottom_right_y) / 2

                w, h = (bottom_right_x - top_left_x), (bottom_right_y - top_left_y) 

                file.write('0 ')
                file.write(str(top_left_x) + ' ')
                file.write(str(top_left_y) + ' ')
                file.write(str(bottom_right_x) + ' ')
                file.write(str(bottom_right_y) + ' ')

                for x, y in points:
                    file.write(str(x) + ' ')
                    file.write(str(y) + ' ')
                    file.write("2 ")
                
                for i in range((17 - len(points)) * 3):
                    file.write("0 ")
                
                file.write("\n")