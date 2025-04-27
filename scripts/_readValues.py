from readAcceleration import getAccelleration
from readCarbon import getCO2
from readGeiger import getGeigerCounts
from readGPS import getPosition
from readOzone import getOzoneConcentration
from readPressure import getPressureData, pressureInit
from readBME import getBMEData
from colorama import Fore
import cv2

from time import sleep


def getSensorValues(pressureCalibrationData):
    acceleration, co2Data, geigerCounts, position, ozone, pressureData = None, None, None, None, None, None
    try:
        acceleration = getAccelleration()
    except:
        print(Fore.RED + "Problem: Acceleration measurement failed")
    try:
        geigerCounts = getGeigerCounts()
    except:
        print(Fore.RED + "Problem: Geiger measurement failed")
    try:
        position = getPosition()
    except:
        print(Fore.RED + "Problem: GPS measurement failed")
    try:
        ozone = getOzoneConcentration()
    except:
        print(Fore.RED + "Problem: Ozone measurement failed")
    try:
        pressureData = getPressureData(pressureCalibrationData)
        precisePressure, _temp = pressureData
        print(precisePressure)
    except:
        precisePressure = None
        print(Fore.RED + "Problem: Pressure measurement failed")
    try:
        co2Data = getCO2(int(precisePressure))
    except Exception as exceptionMsg:
        print(Fore.RED + "Problem: CO2 measurement failed:", exceptionMsg)
    try:
        bmeData = getBMEData()
    except:
        print(Fore.RED + "Problem: AHT measurement failed")


    return acceleration, geigerCounts, position, ozone, pressureData, co2Data, bmeData
    #return ozone
    



