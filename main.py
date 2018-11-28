"""
CHI8 Runner

Usage:
	main.py <filename>
"""

from docopt import docopt
from ui import UI
from random import randint
from threading import Thread
from rpyc.utils.server import ThreadedServer
import rpyc

from ROM import ROM

# u = UI()

def cb(self):
    self.update([randint(0,255) for _ in range(256)])

# u.callback = cb
arguments = docopt(__doc__)
romfile = arguments["<filename>"]
r = ROM(romfile)
r.cycle()

#
# if __name__ == "__main__":
#     def start_thread(service):
#         print(f"Started {service.__name__}")
#         s = ThreadedServer(service, auto_register=True)
#         s.start()
#
#     for service in [UI]:
#         t = Thread(target=start_thread, args=[service])
#         t.start()
#
#
#
#
# ui.root.run()

