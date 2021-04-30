from model.Vertex import Vertex
from model.Plane import Plane
from model.Solid import Solid
import numpy as np


class Vmf(object):
    def __init__(self):
        self.solids = []
        self.ladders = []  # TODO refactor entity class inheritance
        self.id = 1
        self.mapversion = 1
        self.classname = 'worldspawn'
        self.detailmaterial = 'detail/detailsprites'
        self.detailvbsp = 'detail.vbsp'
        self.maxpropscreenwidth = -1
        self.skyname = 'sky_dust'

    def gen_solid(self, centre: Vertex, xr: int, yr: int, zr: int, mflag=False, material="TOOLS/TOOLSNODRAW") -> Solid:
        v1 = Vertex(centre.x-int(xr/2), centre.y+int(yr/2),
                    centre.z+int(zr/2))  # up-back-left
        v2 = Vertex(centre.x-int(xr/2)+xr, centre.y+int(yr/2),
                    centre.z+int(zr/2))  # up-back-right
        v3 = Vertex(centre.x-int(xr/2), centre.y+int(yr/2)-yr,
                    centre.z+int(zr/2))  # up-front-left
        v4 = Vertex(centre.x-int(xr/2)+xr, centre.y+int(yr/2)-yr,
                    centre.z+int(zr/2))  # up-front-right
        v5 = Vertex(centre.x-int(xr/2), centre.y+int(yr/2),
                    centre.z+int(zr/2)-zr)  # down-back-left
        v6 = Vertex(centre.x-int(xr/2)+xr, centre.y+int(yr/2),
                    centre.z+int(zr/2)-zr)  # down-back-right
        v7 = Vertex(centre.x-int(xr/2), centre.y+int(yr/2)-yr,
                    centre.z+int(zr/2)-zr)  # down-front-left
        v8 = Vertex(centre.x-int(xr/2)+xr, centre.y+int(yr/2)-yr,
                    centre.z+int(zr/2)-zr)  # down-front-right
        # p1 = Plane(v1, v2, v4, material)  # up
        if not mflag:
            p1 = Plane(
                v1, v2, v4, "realworldtextures2/concrete/concrete_38")  # up
        else:
            p1 = Plane(v1, v2, v4, "campus/concrete/stone_floor01")  # up

        #p2 = Plane(v7, v8, v6)  # down ##### FORCE NODRAW #####
        p2 = Plane(v7, v8, v6, material)  # down
        p3 = Plane(v1, v3, v7, material)  # left
        p4 = Plane(v6, v8, v4, material)  # right
        p5 = Plane(v2, v1, v5, material)  # back
        p6 = Plane(v8, v7, v3, material)  # front
        vertexList = [v1, v2, v3, v4, v5, v6, v7, v8]
        radiusEvaluate = []
        for v in vertexList:
            radiusEvaluate.append(
                np.sqrt((v.x - centre.x) ** 2 + (v.y - centre.y) ** 2 + (v.z - centre.z) ** 2))
        radius = int(max(radiusEvaluate))
        return Solid(p1, p2, p3, p4, p5, p6, centre, radius, xr, yr, zr)

    def checkCollisionAABB(self, solid: Solid) -> bool:
        if not self.solids:
            return False

        for s in self.solids:
            # x val
            sMinX = s.origin.x-(1/2)*s.xr
            solidMinX = solid.origin.x - (1 / 2) * solid.xr
            sMaxX = s.origin.x+(1/2)*s.xr
            solidMaxX = solid.origin.x + (1 / 2) * solid.xr
            # y val
            sMinY = s.origin.y-(1/2)*s.yr
            solidMinY = solid.origin.y - (1 / 2) * solid.yr
            sMaxY = s.origin.y+(1/2)*s.yr
            solidMaxY = solid.origin.y + (1 / 2) * solid.yr
            # z val
            sMinZ = s.origin.z-(1/2)*s.zr
            solidMinZ = solid.origin.z - (1 / 2) * solid.zr
            sMaxZ = s.origin.z+(1/2)*s.zr
            solidMaxZ = solid.origin.z + (1 / 2) * solid.zr
            # bool check
            checkX = sMinX < solidMaxX and sMaxX > solidMinX
            checkY = sMinY < solidMaxY and sMaxY > solidMinY
            checkZ = sMinZ < solidMaxZ and sMaxZ > solidMinZ

            if (checkX and checkY and checkZ):
                return True
        return False

    def checkCollisionSphere(self, solid: Solid) -> bool:
        if not self.solids:
            return False

        for s in self.solids:
            originPairDistance = int(np.sqrt((s.origin.x - solid.origin.x) ** 2 + (
                s.origin.y - solid.origin.y) ** 2 + (s.origin.z - solid.origin.z) ** 2))

            if (originPairDistance < s.radius + solid.radius):
                return True
        return False

    def add_solid(self, centre: Vertex, xr: int, yr: int, zr: int, material="TOOLS/TOOLSNODRAW", mflag=False, checkCollisionType=0) -> bool:
        solid_evaluate = self.gen_solid(centre, xr, yr, zr, mflag, material)

        if (checkCollisionType == 0):
            # don't check for collision, just add
            self.solids.append(solid_evaluate)
            return True
        elif (checkCollisionType == 1):
            # check for collsion via sphere
            if not self.checkCollisionSphere(solid_evaluate):
                self.solids.append(solid_evaluate)
                return True
        elif (checkCollisionType == 2):
            # check for collsion via aabb
            if not self.checkCollisionAABB(solid_evaluate):
                self.solids.append(solid_evaluate)
                return True
        return False

    def get_pre_string(self):
        # versioninfo
        out_str = 'versioninfo\n{\n'
        out_str += '\t\"editoversion\" \"400\"\n'
        out_str += '\t\"editorbuild\" \"8456\"\n'
        out_str += '\t\"mapversion\" \"5\"\n'
        out_str += '\t\"formatversion\" \"100\"\n'
        out_str += '\t\"prefab\" \"0\"\n}\n'
        # visgroup
        out_str += 'visgroup\n{\n}\n'
        # viewsettings
        out_str += 'viewsettings\n{\n'
        out_str += '\t\"bSnapToGrid\" \"1\"\n'
        out_str += '\t\"bShowGrid\" \"1\"\n'
        out_str += '\t\"bShowLogicalGrid\" \"0\"\n'
        out_str += '\t\"nGridSpacing\" \"64\"\n'
        out_str += '\t\"bShow3DGrid\" \"0\"\n}\n'
        return out_str

    def get_post_string(self):
        ''' TODO
        entity water_lod_control
        entity env_cubemap
        entity color_correction
        entity light_environment
        entity postprocess_controller
        entity env_tonemap_controller
        entity logic_auto
        entity env_sun
        '''
        # cameras
        out_str = 'camera\n{\n'
        out_str += '\t\"activecamera\" \"-1\"\n}\n'
        # cordons
        out_str += 'cordons\n{\n'
        out_str += '\t\"active\" \"0\"\n}'
        return out_str

    def __str__(self):
        # pre string
        out_str = self.get_pre_string()
        out_str += 'world\n{\n'
        out_str += f'\t\"id\" \"{self.id}\"\n'
        out_str += f'\t\"mapversion\" \"{self.mapversion}\"\n'
        out_str += f'\t\"classname\" \"{self.classname}\"\n'
        out_str += f'\t\"detailmaterial\" \"{self.detailmaterial}\"\n'
        out_str += f'\t\"idetailvbspd\" \"{self.detailvbsp}\"\n'
        out_str += f'\t\"maxpropscreenwidth\" \"{self.maxpropscreenwidth}\"\n'
        out_str += f'\t\"skyname\" \"{self.skyname}\"\n'
        # solids
        for i in self.solids:
            out_str += f'{str(i)}\n'
        out_str += '}\n'
        # entities
        # post string
        out_str += self.get_post_string()
        return out_str
