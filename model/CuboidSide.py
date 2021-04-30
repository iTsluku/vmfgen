from model.Vertex import Vertex


class CuboidSide(object):
    def __init__(self, origin: Vertex, xr: int, yr: int, zr: int, direction: int):
        # self.origin = origin
        # self.xr = xr
        # self.yr = yr
        # self.zr = zr
        # TODO enum [1,2,3,4,5,6]->[+x,-y,-x,+y,+z,-z]
        self.direction = direction

        if (direction == 1):
            self.origin = Vertex(origin.x + (1 / 2) * xr, origin.y, origin.z)
            self.height = zr
            self.width = yr
        elif (direction == 2):
            self.origin = Vertex(origin.x, origin.y - (1 / 2) * yr, origin.z)
            self.height = zr
            self.width = xr
        elif (direction == 3):
            self.origin = Vertex(origin.x - (1 / 2) * xr, origin.y, origin.z)
            self.height = zr
            self.width = yr
        elif (direction == 4):
            self.origin = Vertex(origin.x, origin.y + (1 / 2) * yr, origin.z)
            self.height = zr
            self.width = xr
        elif (direction == 5):
            self.origin = Vertex(origin.x, origin.y, origin.z + (1 / 2) * zr)
            self.height = yr
            self.width = xr
        elif (direction == 6):
            self.origin = Vertex(origin.x, origin.y, origin.z - (1 / 2) * zr)
            self.height = yr
            self.width = xr
