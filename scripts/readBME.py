import board
import busio
from time import sleep
from adafruit_bme280 import basic as adafruit_bme280
import smbus2


i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.mode = adafruit_bme280.MODE_NORMAL

def getBMEData():
    return bme280.temperature, bme280.humidity, bme280.relative_humidity, bme280.pressure, bme280.altitude