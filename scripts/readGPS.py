from Libraries.gpsSensor.NEOM8N import *

gpsSensor = NEOM8N()

def getPosition():
    lat, lon, alt = gpsSensor.getPosition()
    return lat, lon, alt
