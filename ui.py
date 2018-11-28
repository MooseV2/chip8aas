import pyglet
from random import randint
from itertools import cycle

class Rect:
    def __init__(self, x, y, w, h):
        self.set(x, y, w, h)

    def draw(self):
        if self._vlist:
            self._vlist.draw(pyglet.gl.GL_QUADS)

    def set(self, x=None, y=None, w=None, h=None, c=0):
        self._x = self._x if x is None else x
        self._y = self._y if y is None else y
        self._w = self._w if w is None else w
        self._h = self._h if h is None else h
        self._quad = ('v2f', (self._x, self._y,
                              self._x + self._w, self._y,
                              self._x + self._w, self._y + self._h,
                              self._x, self._y + self._h))
        self._color = ('c3B', (c, c, c, c, c, c, c, c, c,  c, c, c))
        self._vlist = pyglet.graphics.vertex_list(4, self._quad, self._color)


    def update_color(self, color):
        self._vlist.colors = [color] * 12

    def __repr__(self):
        return f"Rect(x={self._x}, y={self._y}, w={self._w}, h={self._h})"

class DisplayBuffer:
    def __init__(self, size=(64,32), dimensions=(10,10)):
        self.rects = []
        for y in range(size[1]):
            for x in range(size[0]):
                r = Rect(x*dimensions[0], (size[1]*dimensions[1])-y*dimensions[1]-dimensions[1], dimensions[0], dimensions[1])
                self.rects.append(r)

    def update_buffer(self, newbuffer):
        newbuffer = [255 if x else 0 for x in newbuffer]
        list(map(lambda fn: fn[0].__call__(fn[1]), zip((r.update_color for r in self.rects), newbuffer)))

    def draw(self):
        for rect in self.rects:
            rect.draw()

class UI:
    W = 64
    H = 32
    def __init__(self, scale=16, fps=30):
        self.window = pyglet.window.Window(width=scale*self.__class__.W, height=scale*self.__class__.H)
        self.display_buffer = DisplayBuffer(size=(self.__class__.W, self.__class__.H), dimensions=(scale, scale))
        self.callback = None
        pyglet.clock.schedule_interval(self.loop, 1.0/fps)

        @self.window.event
        def on_draw():
            self.window.clear()
            self.display_buffer.draw()

    def loop(self, dt):
        if callable(self.callback):
            self.callback.__call__(self)


    def update(self, buffer):
        self.display_buffer.update_buffer(self.bytes_to_bits(buffer))

    def run(self):
        pyglet.app.run()

    def bytes_to_bits(self, bytelist):
        bits = []
        [bits.extend(map(int, [x for x in '{:08b}'.format(byte)])) for byte in bytelist]
        return bits


if __name__ == "__main__":
    ui = UI()
    from rpyc import connect_by_service
    memory_connection = connect_by_service("memory")
    frame_limiter = cycle(range(10)) # Number of frames between screen update
    def cb(self):
        global memory_connection, frame_limiter
        if next(frame_limiter) == 0:
            buf = memory_connection.root.get_address(0xF00, 256)
            ui.update(buf)
        timers = memory_connection.root.decrement_timers()


    ui.callback = cb
    ui.run()