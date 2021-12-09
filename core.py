import cv2
import numpy as np
from numpy.lib.polynomial import poly
import os
from config import AREA_THRESHOLD, CAR_AVERAGE_COMPRIMENT, PARK_PLOT_COMPRIMENT
from shapely.geometry import Polygon, MultiPolygon
from shapely import affinity

def bounding_box_polygon(bounding_box):
    BB_X=0
    BB_Y=1
    BB_WIDTH=2
    BB_HEIGHT=3

    return Polygon([
            [bounding_box[BB_X], bounding_box[BB_Y]], 
            [bounding_box[BB_X]+bounding_box[BB_WIDTH], bounding_box[BB_Y]],
            [bounding_box[BB_X]+bounding_box[BB_WIDTH], bounding_box[BB_HEIGHT]+bounding_box[BB_Y]],
            [bounding_box[BB_X], bounding_box[BB_HEIGHT]+bounding_box[BB_Y]]
        ])

def get_scale_factor():
    return PARK_PLOT_COMPRIMENT/CAR_AVERAGE_COMPRIMENT

def load_polygons(park_area_info_path):
    POINT = 0
    X = 1
    Y = 2
    NEXT_POINT=3

    polygons = []
    for polygon in os.listdir(park_area_info_path):
        file = open("{}/{}".format(park_area_info_path, polygon), "r")
        lines = file.readlines()
        points = []
        for line in lines:
            data = line.split(" ")
            points.append([int(data[X]), int(data[Y])])
        file.close()
        polygons.append(points)
    return polygons

def draw_polygon(image, polygons):
    for points in polygons:
        points = np.array(points)
        points.reshape((-1,1,2))
        cv2.fillPoly(image, [points], color=(0,0,255))

def detect_intersection(polygon, bounding_boxes):
    p1 = Polygon(polygon)
    polygons_intersections = []
    for bounding_box in bounding_boxes:
        p2 = bounding_box_polygon(bounding_box=bounding_box)
        polygons_intersections.append(list(p1.intersection(p2).exterior.coords))

    return polygons_intersections

def draw_free(polygons_intersections, image):
    X = 0
    Y = 1
    for polygon in polygons_intersections:
        polygon_array = []
        for coord in polygon:
            polygon_array.append([round(coord[X]), round(coord[Y])])
        if(len(polygon_array)>0):
            polygon_array = np.array(polygon_array)
            cv2.fillPoly(image, [polygon_array], color=(0,255,0))

def free_spots(polygons_points, bounding_boxes):
    polygons = [Polygon(x) for x in polygons_points]
    p1 = MultiPolygon(polygons)
    polygons_points=[]
    fact = get_scale_factor()
    for bounding_box in bounding_boxes:
        p2 = affinity.scale(bounding_box_polygon(bounding_box=bounding_box), xfact=fact, yfact=fact)
        p1 = p1.difference(p2)
    if type(p1) is MultiPolygon:
        for p in p1:
            polygons_points.append(list(p.exterior.coords))
    else:
        polygons_points.append(list(p1.exterior.coords))

    return polygons_points

def verify_free_spots(polygons):
    if(len(polygons)==0):
        print("Não há vagas livres de estacionamento")
    else:
        print("Há vagas livres de estacionamento")
