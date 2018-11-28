from rpyc import connect_by_service
import pantograph
from threading import Thread
from time import sleep
import asyncio

# TODO: Major fault handling

class UI(pantograph.PantographHandler):
	W = 64
	H = 32
	CW = 10 # Cell width
	CH = 10

	def setup(self):
		self.keys = [ord(x) for x in '1234QWERASDFZXCV']
		self.pressed_keys = set()
		self.rects = self.rects = [0]*(UI.W*UI.H)
		self.memory = UIServer.memory
		assert self.memory
		# self.memory = connect_by_service("memory")
		
	def update(self):
		refresh = self.memory.root.get_refresh()
		if not refresh: return
		self.rects = self.bytes_to_bits(self.memory.root.get_address(0xF00, 256))
		self.memory.root.set_refresh(False)
		for y in range(UI.H):
			for x in range(UI.W):
				self.fill_rect(x*UI.CW, y*UI.CH, UI.CW, UI.CH, "#FFF" if self.rects[y*UI.W+x] else "#000")

	def get_keys(self):
		keylist = ""
		for key in self.keys:
			if key in self.pressed_keys:
				keylist += "1"
			else:
				keylist += "0"
		return int(keylist, 2)

	def on_key_down(self, event):
		# print(f"KEYD: {event.key_code}")
		if event.key_code in self.keys:
			self.pressed_keys.add(event.key_code)
			self.memory.root.set_io_keys(self.get_keys())

	def on_key_up(self, event):
		# print(f"KEYU: {event.key_code}")
		if event.key_code in self.keys:
			self.pressed_keys.remove(event.key_code)
			self.memory.root.set_io_keys(self.get_keys())

	def bytes_to_bits(self, bytelist):
		bits = []
		[bits.extend(map(int, [x for x in '{:08b}'.format(byte)])) for byte in bytelist]
		return bits


class UIServer(Thread):
	memory = None
	def __init__(self, memory):
		Thread.__init__(self)
		UIServer.memory = memory
		self.app = pantograph.SimplePantographApplication(UI)

	def run(self):
		print("Starting UI thread")
		asyncio.set_event_loop(asyncio.new_event_loop())
		self.app.run()


if __name__ == "__main__":
    app = pantograph.SimplePantographApplication(UI)
    app.run()