from rpyc.utils.server import ThreadedServer
import rpyc

if __name__ == "__main__":

    get_class = rpyc.connect_by_service("GET")
    time = get_class.root.get_time_service()

    s = ThreadedServer(time, auto_register=True, protocol_config = {"allow_public_attrs" : True})
    s.start()
