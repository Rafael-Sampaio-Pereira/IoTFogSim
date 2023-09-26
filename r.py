
from datetime import datetime, date, time, timedelta


def readable_time_to_seconds(hours, minutes):
    timeobj = time(hours, minutes)
    t = datetime.combine(date.min, timeobj) - datetime.min
    isinstance(t, timedelta)
    time_in_seconds = str(t.total_seconds()).split('.')[0]
    return int(time_in_seconds)


print(readable_time_to_seconds(00,00))