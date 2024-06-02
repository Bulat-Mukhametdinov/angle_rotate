import matplotlib.pyplot as plt
import torch
import cv2
from torchvision import transforms
import numpy as np
from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint, plot_skeleton_kpts

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
weigths = torch.load('best.pt', map_location=device)
model = weigths['model']
_ = model.float().eval()

if torch.cuda.is_available():
    model.half().to(device)

image = cv2.imread('./test.jpg')
image = cv2.resize(image, (640, 640))
image_ = image.copy()
image = transforms.ToTensor()(image)
image = torch.tensor(np.array([image.numpy()]))

if torch.cuda.is_available():
    image = image.half().to(device)   
output, _ = model(image)

output = non_max_suppression_kpt(output, 0.15, 0.45, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'], kpt_label=True)
with torch.no_grad():
    output = output_to_keypoint(output)


output /= 640

with open("predictions.txt", 'w') as w:
    if len(output) == 0:
        w.write('')
    else:
        w.writelines('\n'.join([' '.join(map(str, list(i))) for i in output[:, 2:18 + 7]]))