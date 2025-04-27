from Libraries.geigerCounter.geigerCounter import *

# Average Value: 28
# Min Value: 14
# Max Value: 43

geiger = GeigerCounter(pin=23)

def getGeigerCounts():
    return(geiger.get_count())