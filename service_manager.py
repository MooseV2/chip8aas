# Divides up tasks
import rpyc
from itertools import cycle
from time import sleep

class ServiceManager:
    def __init__(self):
        self.services = {}
        available_services = ["memory", "maths", "flow", "bitop", "draw", "misc"]
        clients = rpyc.discover("WAITFORSERVICES")
        print(f"Found {len(clients)} clients")

        client_list = []
        for (ip, port) in clients:
            try:
                client = rpyc.connect(ip, port=port)
                client_list.append(client)
            except Exception:
                print(f"Client [{ip}]:{port} is unreachable. Dead?")
        print(f"Usable clients: {len(client_list)}")

        usable_clients = cycle(client_list)
        allocated_clients = {}
        for item in available_services:
            alloc_client = next(usable_clients)
            print(f"{item} allocated to {alloc_client.root.get_hostname()}")
            alloc_client.root.add_service("Services." + item)

        services_left = set(available_services)
        while len(services_left) > 0:
            try:
                service = services_left.pop()
                self.services[service] = rpyc.connect_by_service(service)
                print(f"Loaded [{service}]")
            except:
                services_left.add(service)
                print(f"Still waiting on [{service}]")
                sleep(0.1)

    def Do(self, name):
        if name in self.services:
            return self.services[name].root
        else:
            print(f"ERROR: Service not found ({name})")

