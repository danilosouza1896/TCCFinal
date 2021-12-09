from xml.etree import ElementTree


def load_expected(f_name):
    document = ElementTree.parse('test/{}.xml'.format(f_name))
    root = document.getroot()
    expecteds = []
    for object in root.findall("object"):
        x_min = int(object.find("bndbox").find("xmin").text)
        y_min = int(object.find("bndbox").find("ymin").text)
        x_max = int(object.find("bndbox").find("xmax").text)
        y_max = int(object.find("bndbox").find("ymax").text)
        w = x_max - x_min
        h = y_max - y_min
        expecteds.append([x_min, y_min, w, h])
    return expecteds

def IoU(expect, bounding_boxes):
    X=0
    Y=1
    W=2
    H=3

    max_value = 0
    for bounding_box in bounding_boxes:
        box_x = bounding_box[X]
        box_y = bounding_box[Y]
        box_w = bounding_box[W]
        box_h = bounding_box[H]

        exp_x = expect[X]
        exp_y = expect[Y]
        exp_w = expect[W]
        exp_h = expect[H]

        w_intersect = min(box_x + box_w, exp_x + exp_w) - max(box_x, exp_x)
        h_intersect = min(box_y + box_h, exp_y + exp_h) - max(box_y, exp_y)

        if w_intersect <=0 or h_intersect <=0:
            continue

        intersection = w_intersect * h_intersect
        union = box_w * box_h + exp_w * exp_h - intersection

        iou = intersection/union

        if(iou>max_value):
            max_value = iou

    return max_value



        