import numpy as np
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import pylab as pl
from PIL import Image

print(os.getcwd())

"""
=====================================     STEP1 START  ======================================
Start of: Read IMG
"""

img0 = "./input/detect-person-on-motorbike-or-scooter/dataset/obj/abc.jpg"
_ = plt.figure(figsize = (20,10))
_ = plt.axis('off')
_ = plt.imshow(mpimg.imread(img0))

directory = './input/detect-person-on-motorbike-or-scooter/dataset/obj/'

imagepath = []  # 이미지 경로 + 파일명
imagefile = []  # 이미지 파일명
boxset = []  # 각 이미지별 박스값
boxfile = []  # 각 이미지별 박스값을 가진 파일명

for im in os.listdir(directory):
    if im[-4:] == '.jpg':
        path = os.path.join(directory, im)
        imagepath += [path]
        imagefile += [im]

for im in imagefile:
    if im[-4:] == '.jpg':
        bx = im[0:-4] + '.txt'
        path = os.path.join(directory, bx)
        if os.path.isfile(path):
            bxdata = np.loadtxt(path)
        boxset += [bxdata]
        boxfile += [bx]

print(imagefile[0:5])
print(boxfile[0:5])
# ['98__flip.jpg', '56__flip.jpg', '140__flip.jpg', '208.jpg', 'IMG_5892.jpg']
# ['98__flip.txt', '56__flip.txt', '140__flip.txt', '208.txt', 'IMG_5892.txt']

print(len(boxset))
print(len(imagepath))
# 795
# 795

num0=0
for i in range(692):
    if imagepath[i]==img0:
        num0=i
        print(i)
# 67


"""
=====================================     STEP1 END  ======================================
"""


## YOLO Detection
"""
=====================================     STEP2 START  ======================================
Start of: Loading YOLO v3 network
"""

# for person on bike
weights0_path = './input/detect-person-on-motorbike-or-scooter/yolov3-obj_final.weights'
configuration0_path = './input/detect-person-on-motorbike-or-scooter/yolov3_pb.cfg'

probability_minimum = 0.5

# Setting threshold for filtering weak bounding boxes
# with non-maximum suppression
threshold = 0.3

network0 = cv2.dnn.readNetFromDarknet(configuration0_path, weights0_path)

# Getting list with names of all layers from YOLO v3 network
layers_names0_all = network0.getLayerNames()

# Check point
print(layers_names0_all)

# Getting only output layers' names that we need from YOLO v3 algorithm
# with function that returns indexes of layers with unconnected outputs
# layers_names0_output = [layers_names0_all[i[0]-1] for i in network0.getUnconnectedOutLayers()]
layers_names0_output = [layers_names0_all[i-1] for i in network0.getUnconnectedOutLayers()]

# Check point
print(layers_names0_output)  # ['yolo_82', 'yolo_94', 'yolo_106']

labels0 = open('./input/detect-person-on-motorbike-or-scooter/coco.names').read().strip().split('\n')
print(labels0)
# ['person_bike']

# for helmet
weights1_path = './input/helmet-detection-yolov3/yolov3-helmet.weights'
configuration1_path = './input/helmet-detection-yolov3/yolov3-helmet.cfg'

network1 = cv2.dnn.readNetFromDarknet(configuration1_path, weights1_path)
layers_names1_all = network1.getLayerNames()
# layers_names1_output = [layers_names1_all[i[0]-1] for i in network1.getUnconnectedOutLayers()]
layers_names1_output = [layers_names1_all[i-1] for i in network1.getUnconnectedOutLayers()]
labels1 = open('./input/helmet-detection-yolov3/helmet.names').read().strip().split('\n')
print(labels1)
# ['Helmet']

"""
=====================================     STEP2 END  ======================================
"""



"""
=====================================     STEP4-1  START ======================================
Start of: Getting blob from current frame
"""

# Getting blob from current frame
# The 'cv2.dnn.blobFromImage' function returns 4-dimensional blob from current
# frame after mean subtraction, normalizing, and RB channels swapping
# Resulted shape has number of frames, number of channels, width and height
image_input = cv2.imread(imagepath[num0])
# blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size, mean, swapRB=True)
blob = cv2.dnn.blobFromImage(image_input,1/255.0,(416,416),swapRB=True,crop=False)

"""
=====================================     STEP4-1  END ======================================
"""

"""
=====================================     STEP4-2 START ======================================
Start of: Implementing Forward pass
"""

# Implementing forward pass with our blob and only through output layers
# Calculating at the same time, needed time for forward pass
blob_to_show = blob[0,:,:,:].transpose(1,2,0)
network0.setInput(blob) # setting blob as input to the network
network1.setInput(blob) # setting blob as input to the network
output_from_network0 = network0.forward(layers_names0_output)
output_from_network1 = network1.forward(layers_names1_output)
np.random.seed(42)

# Generating colours for representing every detected object
# with function randint(low, high=None, size=None, dtype='l')
colours0 = np.random.randint(0,255,size=(len(labels0),3),dtype='uint8')
colours1 = np.random.randint(0,255,size=(len(labels1),3),dtype='uint8')

print(colours0)
print(colours1)
# [[102 220 225]]
# [[179  61 234]]

"""
=====================================     STEP4-2 END ======================================
"""



"""
=====================================     STEP5 START ======================================
Start of: Getting bounding boxes
"""

# Preparing lists for detected bounding boxes, obtained confidences and class's number
bounding_boxes0 = []
confidences0 = []
class_numbers0 = []

bounding_boxes1 = []
confidences1 = []
class_numbers1 = []

h, w = image_input.shape[:2]

# Going through all output layers after feed forward pass
for result in output_from_network0:
    # Going through all detections from current output layer
    for detection in result:
        # Getting 80 classes' probabilities for current detected object
        scores = detection[5:]
        # Getting index of the class with the maximum value of probability
        class_current = np.argmax(scores)
        # Getting value of probability for defined class
        confidence_current = scores[class_current]

        # Every 'detected_objects' numpy array has first 4 numbers with
        # bounding box coordinates and rest 80 with probabilities
        # for every class
        # print(detected_objects.shape)  # (85,)

        # Eliminating weak predictions with minimum probability
        if confidence_current > probability_minimum:
            # Scaling bounding box coordinates to the initial frame size
            # YOLO data format keeps coordinates for center of bounding box
            # and its current width and height
            # That is why we can just multiply them elementwise to the width and height
            # of the original frame and in this way get coordinates for center
            # of bounding box, its width and height for original frame
            box_current = detection[0:4] * np.array([w, h, w, h])

            # Now, from YOLO data format, we can get top left corner coordinates that are x_min and y_min
            x_center, y_center, box_width, box_height = box_current.astype('int')
            x_min = int(x_center - (box_width / 2))
            y_min = int(y_center - (box_height / 2))

            # Adding results into prepared lists
            bounding_boxes0.append([x_min, y_min, int(box_width), int(box_height)])
            confidences0.append(float(confidence_current))
            class_numbers0.append(class_current)


for result in output_from_network1:
    for detection in result:
        scores = detection[5:]
        class_current = np.argmax(scores)
        confidence_current = scores[class_current]
        if confidence_current > probability_minimum:
            print("confidence_current = ", confidence_current)
            box_current = detection[0:4] * np.array([w, h, w, h])
            x_center, y_center, box_width, box_height = box_current.astype('int')
            x_min = int(x_center - (box_width / 2))
            y_min = int(y_center - (box_height / 2))

            bounding_boxes1.append([x_min, y_min, int(box_width), int(box_height)])
            confidences1.append(float(confidence_current))
            class_numbers1.append(class_current)

"""	
=====================================     STEP5 END ======================================
"""

"""
=====================================     STEP6 START  ======================================
Start of: Non-maximum suppression
"""

# Implementing non-maximum suppression of given bounding boxes
# With this technique we exclude some of bounding boxes if their
# corresponding confidences are low or there is another
# bounding box for this region with higher confidence

# It is needed to make sure that data type of the boxes is 'int'
# and data type of the confidences is 'float'
results0 = cv2.dnn.NMSBoxes(bounding_boxes0,confidences0,probability_minimum,threshold)

"""
=====================================     STEP6 END  ======================================
"""

"""
=====================================     STEP7 START  ======================================
Start of: Drawing bounding boxes and labels
"""

# Checking if there is at least one detected object after non-maximum suppression
if len(results0) > 0:
    # Going through indexes of results
    for i in results0.flatten():
        # Getting current bounding box coordinates, its width and height
        x_min,y_min=bounding_boxes0[i][0],bounding_boxes0[i][1]
        box_width,box_height= bounding_boxes0[i][2],bounding_boxes0[i][3]

        # Preparing colour for current bounding box and converting from numpy array to list
        colour_box_current=[int(j) for j in colours0[class_numbers0[i]]]

        # Drawing bounding box on the original current frame
        cv2.rectangle(image_input,(x_min,y_min),(x_min+box_width,y_min+box_height),colour_box_current,5)

        # Preparing text with label and confidence for current bounding box
        text_box_current0='{}: {:.4f}'.format(labels0[int(class_numbers0[i])],confidences0[i])

        # Putting text with label and confidence on the original image
        cv2.putText(image_input,text_box_current0,(x_min,y_min-7),cv2.FONT_HERSHEY_SIMPLEX,1.5,colour_box_current,5)

results1 = cv2.dnn.NMSBoxes(bounding_boxes1,confidences1,probability_minimum,threshold)


if len(results1) > 0:
    for i in results1.flatten():
        x_min,y_min=bounding_boxes1[i][0],bounding_boxes1[i][1]
        box_width,box_height= bounding_boxes1[i][2],bounding_boxes1[i][3]
        colour_box_current=[int(j) for j in colours1[class_numbers1[i]]]
        cv2.rectangle(image_input,(x_min,y_min),(x_min+box_width,y_min+box_height),colour_box_current,5)
        text_box_current1='{}: {:.4f}'.format(labels1[int(class_numbers1[i])],confidences1[i])
        cv2.putText(image_input,text_box_current1,(x_min,y_min-7),cv2.FONT_HERSHEY_SIMPLEX,1.5,colour_box_current,5)

"""
=====================================     STEP7 END  ======================================
"""


#
# %matplotlib inline
plt.rcParams['figure.figsize'] = (15.0,15.0)
plt.imshow(cv2.cvtColor(image_input,cv2.COLOR_BGR2RGB))
plt.show()