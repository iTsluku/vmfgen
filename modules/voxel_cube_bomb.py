from model.Vmf import Vmf
from model.Vertex import Vertex
from model.CuboidSide import CuboidSide
import random


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
            add_success = vmf.add_solid(Vertex(side.origin.x-(1 / 2) * new_cuboid_dir_length,
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
