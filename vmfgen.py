import random
import numpy as np
from sympy import prime
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D


class Vertex(object):
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'({self.x} {self.y} {self.z})'


class Plane(object):
    id = 1

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
        out_str += '\t\t}'
        return out_str


class Editor(object):
    def __init__(self):
        self.color = '0 143 192'
        self.visgroupshown = 1
        self.visgroupautoshown = 1

    def __str__(self):
        out_str = 'editor\n\t\t{\n'
        out_str += f'\t\t\t\"color\" \"{self.color}\"\n'
        out_str += f'\t\t\t\"visgroupshown\" \"{self.visgroupshown}\"\n'
        out_str += f'\t\t\t\"visgroupautoshown\" \"{self.visgroupautoshown}\"\n'
        out_str += '\t\t}\n'
        return out_str


class Solid(object):
    id = 1

    def __init__(self, p1: Plane, p2: Plane, p3: Plane, p4: Plane, p5: Plane, p6: Plane, origin: Vertex, radius: float, xr: int, yr: int, zr: int):
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


# TODO redfactor: entity class inheritance
class Ladder(object):
    id = 1

    # TODO gen solid ladder textured
    def __ini__(self, origin: Vertex):
        self.id = Ladder.id
        Ladder.id += 1
        self.classname = classname
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

#####
# def algs
#####


def longdong(t: float, a: float) -> tuple[int, int]:
    tmin = 0
    tmax = 3.8
    assert (t >= tmin and t <= tmax), "Error! t range in longdong."
    if (t < 1):
        x = -2/3 * a + a/3 * np.cos(2*np.pi * t + 0.1*np.pi)
        y = -2/3 * a + a/3 * np.sin(2*np.pi * t + 0.1*np.pi)
    elif (t < 5/3):
        x = -1/3*a
        y = -2/3*a + 2*a*(t-1)
    elif (t < 13/6):
        x = - a/3 * np.cos(2*np.pi * (t-5/3))
        y = 2/3 * a + a/3 * np.sin(2*np.pi * (t-5/3))
    elif (t < 17/6):
        x = 1/3*a
        y = 2/3*a - 2*a*(t-13/6)
    else:
        x = 2/3 * a + a/3 * np.cos(2*np.pi * (t-17/6) + np.pi)
        y = -2/3 * a + a/3 * np.sin(2*np.pi * (t-17/6) + np.pi)
    return (int(x), int(y))


def alg_nils(vmf: Vmf):
    # cfg
    n = 100
    a = 2**10
    z = 0
    z_inc = 42
    xrange = 96
    yrange = 96
    zrange = 42
    tmin = 0
    tmax = 3.8
    for t in np.linspace(tmin, tmax, n):
        x, y = longdong(t, a)
        vmf.add_solid(Vertex(x, y, z), xrange, yrange, zrange)
        z += z_inc


class Polar(object):
    def __init__(self, r: float, phi: float):
        self.r = r
        self.phi = phi % 2 * np.pi
        self.x = int(r * np.cos(np.degrees(phi)))
        self.y = int(r * np.sin(np.degrees(phi)))


def alg_prime_spiral(vmf: Vmf):
    # cfg
    texture_t1 = "realworldtextures2/concrete/concrete_37"
    texture_t2 = "realworldtextures2/concrete/concrete_38"
    prime_start = 24
    prime_range = 256
    xrange = 32
    yrange = 32
    zrange = 8
    z = 0
    z_inc = 2
    # prime numbers
    p_list = []
    for i in range(prime_start, prime_range+prime_start):
        p_list.append(prime(i))
    # gen solids
    index = 1
    for p in p_list:
        polar = Polar(p, p)
        if (index % 2 == 0):
            material = texture_t1
        else:
            material = texture_t2
        vmf.add_solid(Vertex(polar.x, polar.y, z),
                      xrange, yrange, zrange, material)
        z += z_inc
        index += 1


def lerp(a, b, x):
    # linear interpolation
    return a + x * (b - a)


def fade(t):
    # 6t^5 -15t^4 +10t^3
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    # grad converts h to the right gradient vector and return the dot product with (x,y)
    vector = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vector[h % 4]
    return g[:, :, 0]*x+g[:, :, 1]*y


def perlin(x, y, seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi+1], xf, yf-1)
    n11 = gradient(p[p[xi+1] + yi+1], xf-1, yf-1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)
    # combine noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)
    return lerp(x1, x2, v)


def alg_perlin_noise_grid(vmf: Vmf):
    # cfg
    texture_t1 = "REALWORLDTEXTURES2/GROUND/SAND_10"
    texture_t2 = "REALWORLDTEXTURES/NEWER/1/DIRT_1_02"
    texture_t3 = "DE_AZTEC/HR_AZTEC/HR_AZTEC_BLEND_GROUNDMUD03-GROUNDROCK04"
    xrange = 128
    yrange = 128
    zrange = 128
    z_noise_scale = 384
    gridsize = 50  # ndarray
    # init noise
    lin = np.linspace(0, 5, gridsize, endpoint=False)
    x, y = np.meshgrid(lin, lin)
    # plt.imshow(perlin(x, y, seed=2), origin='upper')
    # plt.show()
    noisegrid = perlin(x, y, seed=2)
    index_row = 0
    index_col = 0
    for row in noisegrid:
        for ele in row:
            x = xrange * index_col + xrange / 2
            y = yrange * index_row - yrange / 2
            z = ele * z_noise_scale
            if ele < -0.35:
                material = texture_t3
            elif ele > 0.2:
                material = texture_t1
            else:
                material = texture_t2
            vmf.add_solid(Vertex(x, y, z), xrange, yrange, zrange, material)
            index_col += 1
        index_row += 1
        index_col = 0


def alg_lorenz_attractor(vmf: Vmf):
    # cfg
    scale_f = 64
    xrange = 32
    yrange = 32
    zrange = 32
    material = "realworldtextures/floor/mixtile/solid/blue1"

    # init
    rho = 28.0
    sigma = 10.0
    beta = 8.0 / 3.0

    def f(state, t):
        x, y, z = state  # Unpack the state vector
        # Derivatives
        return sigma * (y - x), x * (rho - z) - y, x * y - beta * z

    state0 = [1.0, 1.0, 1.0]
    t = np.arange(0.0, 40.0, 0.01)

    states = odeint(f, state0, t)

    # fig = plt.figure()
    # ax = fig.gca(projection="3d")
    # ax.plot(states[:, 0], states[:, 1], states[:, 2])
    # plt.draw()
    # plt.show()

    for s in states:
        x = int(s[0]) * scale_f
        y = int(s[1]) * scale_f
        z = int(s[2]) * scale_f
        vmf.add_solid(Vertex(x, y, z), xrange, yrange, zrange, material)


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


def alg_voxel_cube_bomb(vmf: Vmf):
    stack = []
    root = vmf.gen_solid(Vertex(0, 0, 0), 1024, 1024, 1024)
    i = root
    vmf.add_solid(i.origin, i.xr, i.yr, i.zr)

    for k in range(1, 7):
        stack.append(CuboidSide(i.origin, i.xr, i.yr, i.zr, k))

    seed = 1337
    material_main = "concrete/hr_c/hr_concrete_wall_001"
    interationCount = 1
    iterationMax = 1000
    assert iterationMax > interationCount
    done = False
    min_size = 96
    swap = True
    dir_up_swap = True
    dir_up_flag = None

    while (stack and (not done)):
        if (interationCount > iterationMax):
            done = True

        side = stack.pop(0)
        random.seed(seed)
        new_cuboid_width = None
        new_cuboid_height = None
        temp_min = min(side.width, side.height)
        min_val = int((temp_min) / 4)

        if (min_val % 2) != 0:
            min_val = min_val+1

        if min_val < min_size:
            min_val = min_size

        new_cuboid_width = random.randint(
            min_val, int(side.width*(5/4)))  # TODO tweak

        if (new_cuboid_width % 2) != 0:
            new_cuboid_width = new_cuboid_width + 1

        new_cuboid_height = random.randint(
            min_val, int(side.height*(5/4)))  # TODO tweak

        if (new_cuboid_height % 2) != 0:
            new_cuboid_height = new_cuboid_height+1

        new_cuboid_dir_length = None

        if swap:
            new_cuboid_dir_length = random.randint(
                min_size, int((new_cuboid_width + new_cuboid_height) * (4/5)))
            swap = not swap
        else:
            new_cuboid_dir_length = random.randint(
                min_size, int((new_cuboid_width + new_cuboid_height) / (3/5)))
            swap = not swap

        if (new_cuboid_dir_length % 2) != 0:
            new_cuboid_dir_length = new_cuboid_dir_length+1

        seed = seed + 1
        interationCount = interationCount + 1
        currentCuboid = None
        add_success = None

        if (side.direction == 1):
            add_success = vmf.add_solid(Vertex(side.origin.x+(1 / 2) * new_cuboid_dir_length,
                                               side.origin.y, side.origin.z), new_cuboid_dir_length, new_cuboid_width, new_cuboid_height, material=material_main, checkCollisionType=2)
            currentCuboid = vmf.gen_solid(Vertex(side.origin.x+(1 / 2) * new_cuboid_dir_length,
                                                 side.origin.y, side.origin.z), new_cuboid_dir_length, new_cuboid_width, new_cuboid_height)
        elif (side.direction == 2):
            add_success = vmf.add_solid(Vertex(side.origin.x, side.origin.y-(1 / 2) * new_cuboid_dir_length,
                                               side.origin.z), new_cuboid_width, new_cuboid_dir_length, new_cuboid_height, material=material_main, checkCollisionType=2)
            currentCuboid = vmf.gen_solid(Vertex(side.origin.x, side.origin.y-(1 / 2) * new_cuboid_dir_length,
                                                 side.origin.z), new_cuboid_width, new_cuboid_dir_length, new_cuboid_height)
        elif (side.direction == 3):
            add_success = collision = vmf.add_solid(Vertex(side.origin.x-(1 / 2) * new_cuboid_dir_length,
                                                           side.origin.y, side.origin.z), new_cuboid_dir_length, new_cuboid_width, new_cuboid_height, material=material_main, checkCollisionType=2)
            currentCuboid = vmf.gen_solid(Vertex(side.origin.x-(1 / 2) * new_cuboid_dir_length,
                                                 side.origin.y, side.origin.z), new_cuboid_dir_length, new_cuboid_width, new_cuboid_height)
        elif (side.direction == 4):
            add_success = vmf.add_solid(Vertex(side.origin.x, side.origin.y+(1 / 2) * new_cuboid_dir_length,
                                               side.origin.z), new_cuboid_width, new_cuboid_dir_length, new_cuboid_height, material=material_main, checkCollisionType=2)
            currentCuboid = vmf.gen_solid(Vertex(side.origin.x, side.origin.y+(1 / 2) * new_cuboid_dir_length,
                                                 side.origin.z), new_cuboid_width, new_cuboid_dir_length, new_cuboid_height)
        elif (side.direction == 5):
            if dir_up_swap:
                dir_up_flag = False
                add_success = vmf.add_solid(Vertex(side.origin.x, side.origin.y, side.origin.z+(1 / 2)
                                                   * new_cuboid_dir_length), new_cuboid_width, new_cuboid_height, new_cuboid_dir_length, material=material_main, checkCollisionType=2)
                currentCuboid = vmf.gen_solid(Vertex(side.origin.x, side.origin.y, side.origin.z+(1 / 2)
                                                     * new_cuboid_dir_length), new_cuboid_width, new_cuboid_height, new_cuboid_dir_length)
                dir_up_swap = not dir_up_swap
            else:
                dir_up_flag = True
                # TODO off center-origin
                amount_failure = 0
                amount_failure_max = 10  # cfg

                while amount_failure < amount_failure_max:
                    min_jumpblock_size = 16
                    new_cuboid_dir_length_add_min = -16
                    new_cuboid_dir_length_add_max = 32
                    new_cuboid_dir_length = new_cuboid_dir_length + \
                        random.randint(new_cuboid_dir_length_add_min,
                                       new_cuboid_dir_length_add_max)

                    new_cuboid_width = random.randint(
                        min_jumpblock_size, int(side.width*(5/4)))  # TODO tweak

                    if (new_cuboid_width % 2) != 0:
                        new_cuboid_width = new_cuboid_width + 1

                    new_cuboid_height = random.randint(
                        min_jumpblock_size, int(side.height*(5/4)))  # TODO tweak

                    if (new_cuboid_height % 2) != 0:
                        new_cuboid_height = new_cuboid_height+1

                    if (new_cuboid_dir_length % 2) != 0:
                        new_cuboid_dir_length = new_cuboid_dir_length + 1

                    if (new_cuboid_dir_length < min_jumpblock_size) or (new_cuboid_dir_length > 256):
                        new_cuboid_dir_length = min_jumpblock_size

                    if (new_cuboid_height / 4 < min_jumpblock_size):
                        new_cuboid_height = min_jumpblock_size
                    else:
                        new_cuboid_height = new_cuboid_height / 4

                        if (new_cuboid_height % 2) != 0:
                            new_cuboid_height = new_cuboid_height + 1

                    if (new_cuboid_width / 4 < min_jumpblock_size):
                        new_cuboid_width = min_jumpblock_size
                    else:
                        new_cuboid_width = new_cuboid_width / 4

                        if (new_cuboid_width % 2) != 0:
                            new_cuboid_width = new_cuboid_width + 1

                    new_cuboid_x_pos = side.origin.x
                    x_min = int(side.origin.x -
                                (1 / 2) * side.width + (1/2)*new_cuboid_width)
                    x_max = int(side.origin.x +
                                (1 / 2) * side.width - (1/2)*new_cuboid_width)
                    new_cuboid_x_pos = random.randint(
                        min(x_min, x_max), max(x_min, x_max))

                    if (new_cuboid_x_pos % 2) != 0:
                        new_cuboid_x_pos = new_cuboid_x_pos + 1

                    new_cuboid_y_pos = side.origin.y
                    y_min = int(side.origin.y -
                                (1 / 2) * side.height + (1/2)*new_cuboid_height)
                    y_max = int(side.origin.y +
                                (1 / 2) * side.height - (1/2)*new_cuboid_height)
                    new_cuboid_y_pos = random.randint(
                        min(y_min, y_max), max(y_min, y_max))

                    if (new_cuboid_y_pos % 2) != 0:
                        new_cuboid_y_pos = new_cuboid_y_pos + 1

                    add_success = vmf.add_solid(Vertex(new_cuboid_x_pos, new_cuboid_y_pos, side.origin.z+(
                        1 / 2) * new_cuboid_dir_length), new_cuboid_width, new_cuboid_height, new_cuboid_dir_length, material="realworldtextures2/marble/marble_02", mflag=True, checkCollisionType=2)

                    if not add_success:
                        amount_failure = amount_failure + 1
                    else:
                        # check for <amount_failure_max> fails in a row
                        amount_failure = 0
                dir_up_swap = not dir_up_swap

        elif (side.direction == 6):
            add_success = vmf.add_solid(Vertex(side.origin.x, side.origin.y, side.origin.z-(1 / 2) * new_cuboid_dir_length),
                                        new_cuboid_width, new_cuboid_height, new_cuboid_dir_length, material=material_main, checkCollisionType=2)
            currentCuboid = vmf.gen_solid(Vertex(side.origin.x, side.origin.y, side.origin.z+(
                1 / 2) * new_cuboid_dir_length), new_cuboid_width, new_cuboid_height, new_cuboid_dir_length)

        if (add_success and (not dir_up_flag)):
            for k in range(1, 7):
                dir_comp = None

                if (side.direction == 1):
                    dir_comp = 3
                elif (side.direction == 2):
                    dir_comp = 4
                elif (side.direction == 3):
                    dir_comp = 1
                elif (side.direction == 4):
                    dir_comp = 2
                elif (side.direction == 5):
                    dir_comp = 6
                elif (side.direction == 6):
                    dir_comp = 5

                if (k != dir_comp):
                    stack.append(CuboidSide(currentCuboid.origin, currentCuboid.xr,
                                            currentCuboid.yr, currentCuboid.zr, k))


def alg_gen_bhop_sphere(vmf: Vmf):
    # cfg
    n = 4000
    min_size = 64
    assert min_size > 8
    max_size = 128
    fail_seq_max = 100
    block_min_distance = 256
    block_xr = min_size
    block_yr = min_size
    block_zr = min_size / 4
    i = 0
    fail_seq_nr = 0
    root = vmf.gen_solid(Vertex(0, 0, 12000), max_size, max_size, max_size)
    solid = root
    vmf.add_solid(solid.origin, solid.xr, solid.yr, solid.zr)

    while i < n or fail_seq_nr >= fail_seq_max:
        skip = False
        # debug
        print(f'{i} / {n}')
        # quick math
        R = solid.radius + block_min_distance
        phi = random.uniform(0, 2*np.pi)
        costheta = random.uniform(-1, 1)
        u = random.uniform(0, 1)
        theta = np.arccos(costheta)
        r = R * np.cbrt(u)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        new_solid_z = int(solid.origin.z + z)
        if new_solid_z % 2 != 0:
            new_solid_z = new_solid_z+1

        if (new_solid_z > solid.origin.z) or (new_solid_z < solid.origin.z-32):
            skip = True

        if not skip:
            new_solid_x = int(solid.origin.x + x)
            if new_solid_x % 2 != 0:
                new_solid_x = new_solid_x + 1

            new_solid_y = int(solid.origin.y + y)
            if new_solid_y % 2 != 0:
                new_solid_y = new_solid_y + 1

            add_success = vmf.add_solid(Vertex(new_solid_x, new_solid_y, new_solid_z), block_xr,
                                        block_yr, block_zr, checkCollisionType=2, material="realworldtextures2/marble/marble_02")

            if add_success:
                i = i + 1
                fail_seq_nr = 0
                # contine on new solid
                solid = vmf.gen_solid(
                    Vertex(new_solid_x, new_solid_y, new_solid_z), block_xr, block_yr, block_zr)
            else:
                fail_seq_nr = fail_seq_nr+1


def execute():
    vmf = Vmf()
    # debug
    # vmf.add_solid(Vertex(0, 0, 0), 50, 53, 21)
    # vmf.add_solid(Vertex(0, 0, 0), 50, 53, 21)
    #####
    # alg_gen_bhop_sphere(vmf)
    alg_voxel_cube_bomb(vmf)
    # alg_lorenz_attractor(vmf)
    # alg_perlin_noise_grid(vmf)
    # alg_prime_spiral(vmf)
    # alg_nils(vmf)
    #####
    f = open('output.vmf', 'r+')
    f.truncate(0)
    f.write(str(vmf))
    f.close()


# RUN
execute()
