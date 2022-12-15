from os.path import basename

import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

print(os.getcwd())

box = pd.read_csv('../data/train_solution_bounding_boxes (1).csv')
# print(box)

sample = cv2.imread('../data/training_images/117.jpg')
# sample = cv2.imread('../data/training_images/vid_4_1780.jpg')
sample = cv2.cvtColor(sample, cv2.COLOR_BGR2RGB)

point = box.iloc[559]
print("point = ", point)
pt1 = (int(point['xmin']), int(point['ymax']))
pt2 = (int(point['xmax']), int(point['ymin']))
print("pt1 = ", pt1, "pt2 = ", pt2)
cv2.rectangle(sample, pt1, pt2, color=(255,0,0), thickness=2)
plt.imshow(sample)
plt.show()


sample = cv2.imread('../data/training_images/vid_4_6320.jpg')
sample = cv2.cvtColor(sample, cv2.COLOR_BGR2RGB)
point = box.iloc[1]
pt1 = (int(point['xmin']), int(point['ymax']))
pt2 = (int(point['xmax']), int(point['ymin']))
cv2.rectangle(sample, pt1, pt2, color=(255,0,0), thickness=2)
plt.imshow(sample)
plt.show()

# Yolo 로드
net = cv2.dnn.readNet("../yolov3.weights", "../yolov3.cfg")
classes = []
with open("../coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
print(net.getUnconnectedOutLayers()) # [200 227 254]

output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
print(output_layers)

# 이미지 가져오기
img = cv2.imread('../data/training_images/vid_4_10000.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, channels = img.shape

blob = cv2.dnn.blobFromImage(img, 1/256, (416, 416), (0, 0, 0), swapRB=True, crop=False)
net.setInput(blob)

# outs는 출력으로 탐지된 개체에 대한 모든 정보와 위치를 제공한다.
outs = net.forward(output_layers)

# 정보를 화면에 표시
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # 좌표
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)


indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)


font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(len(boxes), 3))

for i in indexes.flatten():
    x, y, w, h = boxes[i]
    print(x, y, w, h)
    label = str(classes[class_ids[i]])
    confidence = str(round(confidences[i], 2))
    color = colors[i]
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), color, 2)
    cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (0, 255, 0), 2)

plt.imshow(img)
# plt.show()


def predict_yolo(img_path):
    # 이미지 가져오기
    img = cv2.imread('../data/testing_images/'+img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 1 / 256, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            print(x, y, w, h)
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), ((x + w), (y + h)), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (0, 255, 0), 2)

        plt.imshow(img)
        plt.show()

    else:
        print('탐지된 물체가 없습니다.')


import glob
import random

# paths = glob.glob('../data/testing_images/vid_5_399.jpg')
pathsList = os.listdir('../data/testing_images/')
print("pathsList = ", pathsList)

i=0
for i in range(5):
    print("i = ", i)
    img_path = random.choice(pathsList)
    print("img_path = ", img_path)

    predict_yolo(img_path)
    i += 1

