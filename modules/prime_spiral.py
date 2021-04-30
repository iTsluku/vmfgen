from sympy import prime
from model.Polar import Polar
from model.Vmf import Vmf
from model.Vertex import Vertex


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
