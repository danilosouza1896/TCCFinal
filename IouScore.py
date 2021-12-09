from os import R_OK
import cv2
import numpy as np
from xml.etree import ElementTree
from IoU import IoU, load_expected

from core import *

classes = []
net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

with open("coco.names", "r") as f:
	classes = [line.strip() for line in f.readlines()]

iou_scores = []
total = 0
detected = 0
files = os.listdir('test')
for f_name in files:
    if f_name.endswith('.xml'):
        image = cv2.imread("test/{}.jpg".format(f_name[:-4]))
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        image_height, image_width, _ = image.shape
        net.setInput(blob)
        outputs = net.forward()
        bounding_boxes = []
        confidences = []
        for detection in outputs:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.4:
                box = detection[:4] * np.array([image_width, image_height, image_width, image_height])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                bounding_boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))

        expecteds = load_expected(f_name)
        for expected in expecteds:
            iou_scores.append(IoU(expected, bounding_boxes))
        
        indices = cv2.dnn.NMSBoxes(bounding_boxes, confidences, 0.5, 0.4)

total = len(iou_scores)
sum_score = 0
for iou_score in iou_scores:
    if(iou_score>0):
        detected=detected+1
        sum_score=sum_score+iou_score

        
average_iou = sum_score/detected
accuracy = detected/total


print("Total:{}".format(total))
print("Detected:{}".format(detected))
print("Accuracy:{}".format(accuracy))
print("Average IoU:{}".format(average_iou))