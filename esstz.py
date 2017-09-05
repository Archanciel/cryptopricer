from datetime import datetime
from pytz import timezone
import time

print("---- Winter time (CET=Central European Time) ----")
dateStr = "2014-02-28 22:28:15"
datetimeObjUnlocalized = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
print('UNL: ' + datetimeObjUnlocalized.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjUnlocalized-->tm_isdst=' + str(datetimeObjUnlocalized.timetuple()[8]))
datetimeObjZH = timezone('Europe/Zurich').localize(datetimeObjUnlocalized)
print('ZH:  ' + datetimeObjZH.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjZH-->tm_isdst=' + str(datetimeObjZH.timetuple()[8]))
print("UTC: " + datetimeObjZH.astimezone(timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S %Z%z"))

print("\n---- Summer time (CEST=Central European Summer Time) ----")
dateStr = "2014-06-28 22:28:15"
datetimeObjUnlocalized = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
print('UNL: ' + datetimeObjUnlocalized.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjUnlocalized-->tm_isdst=' + str(datetimeObjUnlocalized.timetuple()[8]))
datetimeObjZH = timezone('Europe/Zurich').localize(datetimeObjUnlocalized)
print('ZH:  ' + datetimeObjZH.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
print('     datetimeObjZH-->tm_isdst=' + str(datetimeObjZH.timetuple()[8]))
print("UTC: " + datetimeObjZH.astimezone(timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S %Z%z"))
