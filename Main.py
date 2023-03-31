import Functions as func
from datetime import datetime

dtmTime = 0

while 1:
    dtmTime, dblWaterLevel = func.get_current_water_level(dtmTime)
    dtmNow = datetime.today()

    print(dtmTime, dblWaterLevel, dtmNow)
