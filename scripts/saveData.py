import csv
import os
from datetime import datetime
import time

def createCSV(filename, columns):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(columns)

def saveData(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        zeit = time.strftime("%Y/%m/%d_%H:%M:%S")
        if len(data) > 3:
            writer.writerow([zeit, data[0], data[1], data[2][0], data[2][1], data[3], data[4][0], data[4][1], data[4][2], data[4][3], data[4][4]])
        else:
            writer.writerow([zeit, data[0], data[1]])

# 