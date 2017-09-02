import datetime
from pytz import timezone

class PriceRequester:
    def explore(self):
        print('\nConverting now ...')
        fmt = "%Y-%m-%d %H:%M:%S %Z%z"

        print('Current time in UTC')
        now_utc = datetime.datetime.now(timezone('UTC'))
        print(now_utc.strftime(fmt))

        print('Convert to US/Pacific time zone')
        now_pacific = now_utc.astimezone(timezone('US/Pacific'))
        print(now_pacific.strftime(fmt))

        print('Convert to Europe/Zurich time zone')
        now_berlin = now_pacific.astimezone(timezone('Europe/Zurich'))
        print(now_berlin.strftime(fmt))


        print('\nLocalizing a date/time')
        date_str = "2014-05-28 22:28:15"
        datetime_obj_naive = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # Wrong way!
        datetime_obj_pacific = datetime_obj_naive.replace(tzinfo=timezone('US/Pacific'))
        print('WRONG')
        print(datetime_obj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

        # Right way!
        datetime_obj_pacific = timezone('US/Pacific').localize(datetime_obj_naive)
        print('RIGHT')
        print(datetime_obj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z"))


        print('\nConverting UTC date to other time zone')
        date_str = "2014-05-28 22:28:15"
        datetime_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
        print('Date in UTC')
        print(datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
        print('Convert to US/Pacific time zone')
        pacificTime = datetime_obj_utc.astimezone(timezone('US/Pacific'))
        print(pacificTime.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
        print('Convert Europe/Zurich time zone')
        zurichTime = datetime_obj_utc.astimezone(timezone('Europe/Zurich'))
        print(zurichTime.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

pr = PriceRequester()
pr.explore()