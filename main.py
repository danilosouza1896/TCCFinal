from os import R_OK
import cv2
import numpy as np
from numpy.lib.polynomial import poly
from shapely.geometry import Polygon

from core import *

classes = []
net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
image = cv2.imread("test3.jpg")
shapes = np.zeros_like(image, np.uint8)
image_height, image_width, _ = image.shape
blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)

with open("coco.names", "r") as f:
	classes = [line.strip() for line in f.readlines()]

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

indices = cv2.dnn.NMSBoxes(bounding_boxes, confidences, 0.5, 0.4)

if len(indices)>0:
    for index in indices.flatten():
        (x, y, w, h) = (bounding_boxes[index][0], bounding_boxes[index][1], bounding_boxes[index][2], bounding_boxes[index][3])
        cv2.rectangle(image, (x, y), (x+w, y+h), thickness=2, color=1)

polygons_points = load_polygons()
draw_polygon(image=shapes, polygons=polygons_points)
#intersections = detect_intersection(polygon_points, bounding_boxes)
intersections = free_spots(polygons_points, bounding_boxes)
draw_free(intersections, shapes)

verify_free_spots(intersections)



out = image.copy()
alpha=0.7
mask=shapes.astype(bool)
out[mask] = cv2.addWeighted(image, alpha, shapes, 1 - alpha, 0)[mask]

out = cv2.resize(out, (960, 540))

cv2.imshow('image', out)
cv2.waitKey(0)
cv2.destroyAllWindows()

