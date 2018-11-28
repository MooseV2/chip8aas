from rpyc.utils.server import ThreadedServer
from time_service import TimeService, DateService
from rpyc import Service
from threading import Thread



if __name__ == "__main__":
    def start_thread(service):
        print(f"Started {service.__name__}")
        s = ThreadedServer(service, auto_register=True)
        s.start()

    for service in [TimeService, DateService]:
        t = Thread(target=start_thread, args=[service])
        t.start()

