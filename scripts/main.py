from _readValues import getSensorValues
from _initSensors import initAllSensors
from cameras import createVideo, createCamera, getImage, overlayImage, image_saver, recordVideosPicam
from time import time, sleep
import cv2
from saveData import createCSV, saveData
from multiprocessing import Process
import readBME

# camLeft = createCamera(2)
# camDown = createCamera(0)
vidLeft = createVideo("VideoLeft")
vidLeftOverlay = createVideo("VideoLeftOverlay")

pressureCalData = initAllSensors()

environmentPath = "environment.csv"
environmentColumns = ['Time', "GeigerCounts", "Ozone", "Pressure", "Temperature", "CO2", "InsideTemp", "Humidity", "Relative Humidity", "Pressure", "Altitude"]
movementPath = "movement.csv"
movementColumns = ['Time', "Acceleration", "Position"]

createCSV(environmentPath, environmentColumns)
createCSV(movementPath, movementColumns)

cam_ports = [0, 2]
processes = []

for port in cam_ports:
    p = Process(target=image_saver, args=(port,))
    p.start()
    processes.append(p)

videoRecorder = Process(target=recordVideosPicam)
videoRecorder.start()
processes.append(videoRecorder)

print("Starting...")
startTime = time()
while 1:
    try:
        if(time()-startTime >= 1):
            startTime = time()
            data = getSensorValues(pressureCalData)
            environmentData = data[1], data[3], data[4], data[5], data[6]
            movementData = data[0], data[2]
            saveData(environmentPath, environmentData)
            saveData(movementPath, movementData)
    except Exception as e:
        print(f"Critical Error: {e}")