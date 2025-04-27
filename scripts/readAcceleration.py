import mpu6050
from time import sleep

mpu6050 = mpu6050.mpu6050(0x69)


def getAccelleration():
    return(mpu6050.get_accel_data())

def getGyro():
    return(mpu6050.get_gyro_data())
