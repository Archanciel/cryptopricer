from datetime import datetime
from pytz import timezone
import time

def timestamp2date(timestamp):
    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z%z"

    # function converts a UTC timestamp into Europe/Zurich Gregorian date
    utcTimeStamp = datetime.fromtimestamp(int(timestamp)).replace(tzinfo=timezone('UTC'))

    return utcTimeStamp.astimezone(timezone('Europe/Zurich')).strftime(DATE_TIME_FORMAT)

timeStampUTC_1 = time.mktime(datetime.utcnow().timetuple())
print(datetime.utcnow().timetuple())
print(timeStampUTC_1)
print(timestamp2date(timeStampUTC_1))
timeStampUTC_2 = time.mktime(datetime.now(timezone('UTC')).timetuple())
print(timeStampUTC_2)
print(timestamp2date(timeStampUTC_2))
print(timeStampUTC_2 - timeStampUTC_1)


# 1504385450.0
# 2017-09-03 00:50:50 CEST+0200   this the right time
# 1504389050.0
# 2017-09-03 01:50:50 CEST+0200
# 3600.0
