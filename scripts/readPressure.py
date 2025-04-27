from Libraries.pressureSensor.MS580301BA import *
import smbus
from time import sleep


def pressureInit():
    bus = smbus.SMBus(1)
    reset_sensor(bus, address=0x77)
    sleep(.1)
    C = read_calibration_data(bus, address=0x77)
    print(C)
    return C

def getPressureData(C):
    bus = smbus.SMBus(1)
    D1 = read_sensor_data(bus, 0x48, address = 0x77)  # Pressure conversion command
    D2 = read_sensor_data(bus, 0x58, address = 0x77)  # Temperature conversion command
    pressure, cTemp, fTemp = calculate_temperature_and_pressure(D1, D2, C)
    return pressure, cTemp

