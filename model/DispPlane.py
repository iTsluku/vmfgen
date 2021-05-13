from model.Vertex import Vertex
from model.Plane import Plane
from model.Dispinfo import Dispinfo


class DispPlane(object):

    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, material="TOOLS/TOOLSNODRAW"):
        self.id = Plane.id
        Plane.id += 1
        self.vertices = [v1, v2, v3]
        self.material = material
        self.uaxis = '[1 0 0 0] 0.25'
        self.vaxis = '[0 -1 0 0] 0.25'
        self.rotation = 0
        self.lightmapscale = 16
        self.smoothing_groups = 0
        self.dispinfo = Dispinfo()

    def __str__(self):
        out_str = 'side\n\t\t{\n'
        out_str += f'\t\t\t\"id\" \"{self.id}\"\n'
        out_str += f'\t\t\t\"plane\" \"{str(self.vertices[0])} {str(self.vertices[1])} {str(self.vertices[2])}\"\n'
        out_str += f'\t\t\t\"material\" \"{self.material}\"\n'
        out_str += f'\t\t\t\"uaxis\" \"{self.uaxis}\"\n'
        out_str += f'\t\t\t\"vaxis\" \"{self.vaxis}\"\n'
        out_str += f'\t\t\t\"rotation\" \"{self.rotation}\"\n'
        out_str += f'\t\t\t\"lightmapscale\" \"{self.lightmapscale}\"\n'
        out_str += f'\t\t\t\"smoothing_groups\" \"{self.smoothing_groups}\"\n'
        # TODO add dispinfo
        out_str += '\t\t}'
        return out_str
