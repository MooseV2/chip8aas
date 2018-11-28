from rpyc import Service
from rpyc.utils.server import ThreadedServer
from importlib import import_module
import traceback
from threading import Thread

class WaitForServicesService(Service):
    def start_thread(self, service):
        s = ThreadedServer(service, auto_register=True)
        print(f"Started {service.__name__}")
        s.start()

    def exposed_add_service(self, service):
        try:
            module = import_module(service)
            service_thread = Thread(target=self.start_thread, args=[module._default])
            service_thread.start()
            return True
        except Exception:
            print(f"Unable to create service {service}")
            traceback.print_exc()
            return False

print("Waiting on services")
run_loop = ThreadedServer(WaitForServicesService, auto_register=True)
run_loop.start()

# TODO: Handle cleanup/deregistration on remote stub close

