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
import ui
from ROM import ROM
import pantograph
import webbrowser



if __name__ == "__main__":
	arguments = docopt(__doc__)
	romfile = arguments["<filename>"]
	rom = ROM(romfile)
	print("Connecting to memory service")
	memory = rpyc.connect_by_service("memory")
	print("Connected to memory")
	UI = ui.UIServer(memory)
	UI.start()
	webbrowser.open("http://localhost:8080")
	rom.cycle()

	

