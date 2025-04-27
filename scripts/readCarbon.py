import time
import board
import adafruit_scd4x


i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
co2Concentration = 0

def carbonInit():
    global co2Concentration
    scd4x.start_periodic_measurement()
    while(not scd4x.data_ready):
        time.sleep(0.001)
    co2Concentration = scd4x.CO2

def getCO2(pressure):
    global co2Concentration

    if pressure is None:
        pressure = 1000
        print("BadPressureMeasurement")
    if scd4x.data_ready:
        co2Concentration = scd4x.CO2
        scd4x.set_ambient_pressure(pressure)
    return co2Concentration
