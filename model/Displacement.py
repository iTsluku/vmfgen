from model.Vertex import Vertex
from model.Solid import Solid
from model.Editor import Editor
from model.Plane import Plane
from model.DispPlane import DispPlane


class Displacement(object):
    id = 1

    def __init__(self, p1: DispPlane, p2: Plane, p3: Plane, p4: Plane, p5: Plane, p6: Plane, origin: Vertex, radius: float, xr: int, yr: int, zr: int):
        self.id = Solid.id
        Solid.id += 1
        self.planes = [p1, p2, p3, p4, p5, p6]
        self.origin = origin
        self.radius = radius  # space occupation, bounding sphere for collision
        self.xr = xr
        self.yr = yr
        self.zr = zr
        self.editor = Editor()

    def __str__(self):
        out_str = '\tsolid\n\t{\n'
        out_str += f'\t\t\"id\" \"{self.id}\"\n'
        for i in self.planes:
            out_str += f'\t\t{str(i)}\n'
        out_str += f'\t\t{str(self.editor)}'
        out_str += '\t}'
        return out_str
