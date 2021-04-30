from model.Vertex import Vertex
from model.Editor import Editor


# TODO redfactor: entity class inheritance
class Ladder(object):
    id = 1

    # TODO gen solid ladder textured
    def __ini__(self, origin: Vertex):
        self.id = Ladder.id
        Ladder.id += 1
        # self.classname = classname
        self.angles = "0 0 0"
        "disableflashlight" "0"
        "disableselfshadowing" "0"
        "disableshadowdepth" "0"
        "disableshadows" "1"
        "disablevertexlighting" "0"
        "disableX360" "0"
        "drawinfastreflection" "0"
        "enablelightbounce" "0"
        "fademaxdist" "0"
        "fademindist" "-1"
        "fadescale" "1"
        "ignorenormals" "0"
        "maxcpulevel" "0"
        "maxgpulevel" "0"
        "mincpulevel" "0"
        "mingpulevel" "0"
        "model" "models/props/de_nuke/hr_nuke/metal_ladder_001/metal_ladder_001_64.mdl"
        "preventpropcombine" "0"
        "renderamt" "255"
        "rendercolor" "255 255 255"
        "screenspacefade" "0"
        "shadowdepthnocache" "0"
        "skin" "0"
        "solid" "0"
        "uniformscale" "1"
        self.origin = f'{str(origin.x)} {str(origin.y)} {str(origin.z)}'
        self.editor = Editor()  # TODO groupid ?

    def __str__(self):
        # TODO add editor + group???
        return ""
