import os
from xml.etree import ElementTree

# Get .txt files
files = os.listdir('dataset/training/')
print(len(files))
car = 0
pedestrian = 0
lines = []
for f_name in files:
    if f_name.endswith('.xml'):
        document = ElementTree.parse('dataset/training/{}'.format(f_name))
        root = document.getroot()
        for object in root.findall("object"):
            if(object.find("name").text!="truck" and object.find("name").text!="misc" and object.find("name").text!="motorcycle"):
                lines.append("dataset/training/{}, {}, {}, {}, {}, {}".format(
                    root.find("filename").text, 
                    int(object.find("bndbox").find("xmin").text),
                    int(object.find("bndbox").find("ymin").text),
                    int(object.find("bndbox").find("xmax").text),
                    int(object.find("bndbox").find("ymax").text),
                    object.find("name").text
                ))
                if object.find("name").text=="car":
                    car=car+1
                elif object.find("name").text=="pedestrian":
                    pedestrian=pedestrian+1

print(pedestrian)
print(car)
join_file = "\n".join(lines)
file_save = open("data.txt", "w")
file_save.write(join_file)