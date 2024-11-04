from easypaint import EasyPaint
import sys
from e2 import Data, Result, process, read_data


class TightRopeViewer(EasyPaint):
    def __init__(self, 
                 buildings: Data,
                 result: Result = None,
                 canvas_width = 1050,
                 canvas_height = 600,
                 unit = 30, offset = 0.5):
        EasyPaint.__init__(self)
        self.buildings = buildings
        self.result = result
        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
        self.unit = unit
        self.offset = offset

    def main(self):
        maxh = self.offset + max(self.buildings) + 1
        width = len(self.buildings)

        if width*self.unit > self._canvas_width:
            self.unit = self._canvas_width // width
        self.easypaint_configure(title="TightRope",
                                 background="white",
                                 size=(self._canvas_width, self._canvas_height),
                                 coordinates=(-1, -1, width, maxh)
                                 )
        if result != None:
            left, right, valley, height = result
            for x, c in [(left, "lightblue"), (valley, "lightgreen"), (right, "lightblue")]:
                self.create_rectangle(x, 0, x+1, self.buildings[x], color="black", fill=c, width=1)
            h = min(self.buildings[left], self.buildings[right])
            self.create_line(left + 1, h, right, h, color="blue", width=2)
            self.create_text(valley + 0.5, h + 0.5, text=str(height), color="black")
        for x, h in enumerate(self.buildings):
            self.create_rectangle(x, 0, x+1, h, color="black", width=1)
            self.create_text(x + 0.5, h + 0.5, text=str(h), color="black")
            self.create_text(x + 0.5, - 0.5, text=str(x), color="black")

    def on_key_press(self, keysym):
        if keysym == 'Escape' or keysym == 'Return':
            self.close()


def read_result(name: str) -> Result:
    with open(name) as f:
        l = f.readline()
        if l == "NO HAY SOLUCIÓN\n":
            return None
        else:
            return tuple(int(x) for x in l.split())


if __name__ == "__main__":
    data = None
    result = None

    for arg in sys.argv[1:]:
        if arg == "-":
            if data is None:
                data = read_data(sys.stdin)
            elif result is None:
                result = read_result(sys.stdin)
            else:
                exit("Too many arguments")
            continue
        if arg == "-s":
            if result is None:
                result = "-s"
            else:
                exit("Too many arguments")
            continue
        if data is None:
            with open(arg) as f:
                data = read_data(f)
        elif result is None:
            result = read_result(arg)
        else:
            exit("Too many arguments")
    if data is None:
        data = read_data(sys.stdin)
    if result == "-s":
        result = process(data)
    viewer = TightRopeViewer(data, result)
    viewer.run()
