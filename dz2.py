from datetime import datetime
from datetime import timedelta


def get_time_intervals(time_start, time_end, timescale):
    time_start = datetime.strptime(time_start, '%H:%M')
    time_end = datetime.strptime(time_end, '%H:%M')
    interval = timedelta(minutes=int(timescale))
    while time_start < time_end:
        print('начало: ' + str(time_start))
        time_start += interval
        if time_start > time_end:
            break
        print('конец: ' + str(time_start))


t1 = '10:02'
t2 = '10:45'
tsc = '15'

get_time_intervals(t1, t2, tsc)
