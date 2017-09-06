from datetime import datetime
from pytz import timezone
import time

print("--H hiver CET=Central European Time--")
dateStr = "2014-02-28 22:28:15"
datetimeObjUnlocalized = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
print('UNL: ' + datetimeObjUnlocalized.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjUnlocalized-->tm_isdst=' + str(datetimeObjUnlocalized.timetuple()[8]))
datetimeObjZH = timezone('Europe/Zurich').localize(datetimeObjUnlocalized)
print('ZH:  ' + datetimeObjZH.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjZH-->tm_isdst=' + str(datetimeObjZH.timetuple()[8]))
datetimeObjUTC = datetimeObjZH.astimezone(timezone('UTC'))
print("UTC: " + datetimeObjUTC.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjUTC-->tm_isdst=' + str(datetimeObjUTC.timetuple()[8]))
datetimeObjGMT = datetimeObjZH.astimezone(timezone('GMT'))
print("GMT: " + datetimeObjGMT.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjGMT-->tm_isdst=' + str(datetimeObjGMT.timetuple()[8]))

print("\n--H été CEST=Central European Summer Time--")
dateStr = "2014-06-28 22:28:15"
datetimeObjUnlocalized = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
print('UNL: ' + datetimeObjUnlocalized.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjUnlocalized-->tm_isdst=' + str(datetimeObjUnlocalized.timetuple()[8]))
datetimeObjZH = timezone('Europe/Zurich').localize(datetimeObjUnlocalized)
print('ZH:  ' + datetimeObjZH.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjZH-->tm_isdst=' + str(datetimeObjZH.timetuple()[8]))
datetimeObjUTC = datetimeObjZH.astimezone(timezone('UTC'))
print("UTC: " + datetimeObjUTC.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjUTC-->tm_isdst=' + str(datetimeObjUTC.timetuple()[8]))
datetimeObjGMT = datetimeObjZH.astimezone(timezone('GMT'))
print("GMT: " + datetimeObjGMT.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjGMT-->tm_isdst=' + str(datetimeObjGMT.timetuple()[8]))