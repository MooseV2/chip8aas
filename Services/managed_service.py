from rpyc import Service, connect_by_service

class ManagedService(Service):
    def __init__(self):
        super()
        self.memory_connection = connect_by_service("memory")
        print(f"Service [{self.__class__.__name__}] found memory")
        self.memory = self.memory_connection.root