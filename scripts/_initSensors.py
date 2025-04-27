from readCarbon import carbonInit
from readOzone import ozoneInit
from readPressure import pressureInit
# from readBME import bmeInit

def initAllSensors():
    carbonInit()
    ozoneInit()
    # bmeInit()
    return pressureInit()
