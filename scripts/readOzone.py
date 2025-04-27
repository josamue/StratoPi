from Libraries.Ozone.DFRobot_Ozone import *

COLLECT_NUMBER   = 20
IIC_MODE         = 0x01
ozone = DFRobot_Ozone_IIC(IIC_MODE ,OZONE_ADDRESS_1)

def ozoneInit():
    ozone.set_mode(MEASURE_MODE_AUTOMATIC)

def getOzoneConcentration():
    return ozone.get_ozone_data(COLLECT_NUMBER)

