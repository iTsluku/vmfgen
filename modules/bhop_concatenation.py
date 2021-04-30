from model.Vmf import Vmf
from model.Vertex import Vertex
import numpy as np
import random


def alg_bhop_concatenation(vmf: Vmf):
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
