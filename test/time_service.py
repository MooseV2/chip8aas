import time
from rpyc import Service
from datetime import datetime
from threading import Thread


class TimeService(Service):
    def exposed_get_utc(self):
        return time.time()

    def exposed_get_time(self):
        print("TIME CALL")
        return time.ctime()

class DateService(Service):
    def exposed_get_date(self):
        print("DATE CALL")
        return datetime.now()