import time
import smbus



def reset_sensor(bus, address=0x76):
    """Send reset command to the sensor."""
    bus.write_byte(address, 0x1E)
    time.sleep(0.1)

def read_calibration_data(bus, address=0x76):
    """Read and return calibration coefficients from the sensor."""
    coefficients = []
    for reg in range(0xA2, 0xAD, 2):
        data = bus.read_i2c_block_data(address, reg, 2)
        coefficients.append(data[0] * 256 + data[1])
    return coefficients

def read_sensor_data(bus, command, address=0x76):
    bus.write_byte(address, command)
    time.sleep(0.01)
    data = bus.read_i2c_block_data(address, 0x00, 3)
    return data[0] * 65536 + data[1] * 256 + data[2]

def calculate_temperature_and_pressure(D1, D2, C):
    """Calculate temperature and pressure based on sensor readings and calibration coefficients."""
    dT = D2 - C[4] * 256
    TEMP = 2000 + dT * C[5] / 8388608
    OFF = C[1] * 65536 + (C[3] * dT) / 128
    SENS = C[0] * 32768 + (C[2] * dT) / 256
    
    T2, OFF2, SENS2 = 0, 0, 0
    if TEMP < 2000:
        T2 = (dT * dT) / 2147483648
        OFF2 = 3 * ((TEMP - 2000) * (TEMP - 2000))
        SENS2 = 7 * ((TEMP - 2000) * (TEMP - 2000)) / 8
        if TEMP < -1500:
            SENS2 += 2 * ((TEMP + 1500) * (TEMP + 1500))
    elif TEMP > 4500:
        SENS2 -= ((TEMP - 4500) * (TEMP - 4500)) / 8
    
    TEMP -= T2
    OFF -= OFF2
    SENS -= SENS2
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0
    cTemp = TEMP / 100.0
    fTemp = cTemp * 1.8 + 32
    
    return pressure, cTemp, fTemp
