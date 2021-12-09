from os import read
from random import randint
import os

from config import LABELS, TRAINING_PATH

items_count=7481
qtdItems=200

file_numbers = list(range(0, items_count))
count = 0

lines = []

CLASS=0
X1=4
Y1=5
X2=6
Y2=7

while(count<qtdItems):
    if qtdItems < items_count:
        sorted_index = randint(0, len(file_numbers)-1)
        sorted = file_numbers[sorted_index]
        file_numbers.remove(sorted)
    else:
        sorted = count

    count=count+1
    file_name = "{:0>6d}".format(sorted)
    file = open(os.path.sep.join([LABELS, "{}.txt".format(file_name)]))
    readed_lines = file.readlines()

    for line in readed_lines:
        split_line = line.split(' ')
        class_name = split_line[CLASS]

        train_file_path = os.path.sep.join([TRAINING_PATH, "{}.png".format(file_name)])
        if split_line[CLASS]=="Car" or split_line=="Truck" or split_line=="Van":
            lines.append("{}, {}, {}, {}, {}, {}".format(
                train_file_path, 
                round(float(split_line[X1])), 
                round(float(split_line[Y1])), 
                round(float(split_line[X2])), 
                round(float(split_line[Y2])),
                split_line[CLASS])
            )


join_file = "\n".join(lines)
file_save = open("data.txt", "w")
file_save.write(join_file)
            