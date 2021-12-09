import os

BASE_PATH = ".."
TRAINING_PATH = os.path.sep.join([BASE_PATH, "training", "image_2"])
LABELS = os.path.sep.join([BASE_PATH, "labels"])

AREA_THRESHOLD = 300

#De acordo com a ABNT, uma vaga de estacionamento paralela ao meio-fio tem um comprimento de 5.5
PARK_PLOT_COMPRIMENT = 5.5

CAR_AVERAGE_COMPRIMENT = 4.0

