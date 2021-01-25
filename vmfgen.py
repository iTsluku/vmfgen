import numpy as np
from sympy import prime
import matplotlib.pyplot as plt


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

    def __init__(self, p1: Plane, p2: Plane, p3: Plane, p4: Plane, p5: Plane, p6: Plane):
        self.id = Solid.id
        Solid.id += 1
        self.planes = [p1, p2, p3, p4, p5, p6]
        self.editor = Editor()

    def __str__(self):
        out_str = '\tsolid\n\t{\n'
        out_str += f'\t\t\"id\" \"{self.id}\"\n'
        for i in self.planes:
            out_str += f'\t\t{str(i)}\n'
        out_str += f'\t\t{str(self.editor)}'
        out_str += '\t}'
        return out_str


class Vmf(object):
    def __init__(self):
        self.solids = []
        self.id = 1
        self.mapversion = 1
        self.classname = 'worldspawn'
        self.detailmaterial = 'detail/detailsprites'
        self.detailvbsp = 'detail.vbsp'
        self.maxpropscreenwidth = -1
        self.skyname = 'sky_dust'

    def gen_solid(self, centre: Vertex, xr: int, yr: int, zr: int, material="TOOLS/TOOLSNODRAW") -> Solid:
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
        p1 = Plane(v1, v2, v4, material)  # up
        p2 = Plane(v7, v8, v6, material)  # down
        p3 = Plane(v1, v3, v7, material)  # left
        p4 = Plane(v6, v8, v4, material)  # right
        p5 = Plane(v2, v1, v5, material)  # back
        p6 = Plane(v8, v7, v3, material)  # front
        return Solid(p1, p2, p3, p4, p5, p6)

    def add_solid(self, centre: Vertex, xr: int, yr: int, zr: int, material="TOOLS/TOOLSNODRAW"):
        solid_evaluate = self.gen_solid(centre, xr, yr, zr, material)
        # TODO check for collisions
        if (True):
            self.solids.append(solid_evaluate)

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
        for i in self.solids:
            out_str += f'{str(i)}\n'
        out_str += '}\n'
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
            c = texture_t1
        else:
            c = texture_t2
        vmf.add_solid(Vertex(polar.x, polar.y, z), xrange, yrange, zrange, c)
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
    xrange = 48
    yrange = 48
    zrange = 48
    z_noise_scale = 384
    gridsize = 75  # ndarray
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
                c = texture_t3
            elif ele > 0.2:
                c = texture_t1
            else:
                c = texture_t2
            vmf.add_solid(Vertex(x, y, z), xrange, yrange, zrange, c)
            index_col += 1
        index_row += 1
        index_col = 0


def execute():
    vmf = Vmf()
    #####
    alg_perlin_noise_grid(vmf)
    # alg_prime_spiral(vmf)
    # alg_nils(vmf)
    #####
    f = open('output.vmf', 'r+')
    f.truncate(0)
    f.write(str(vmf))
    f.close()


# RUN
execute()
