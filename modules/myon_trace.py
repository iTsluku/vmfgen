import numpy as np
import matplotlib.pyplot as plt
from model.Vmf import Vmf
from model.Vertex import Vertex

plot = False
gen = True


def little_test(n):
    x = np.zeros(n)
    y = np.zeros(n)
    z = np.zeros(n)
    theta = np.zeros(n)
    phi = np.zeros(n)
    # ds=0.001
    ds = 3
    s = 1
    sd = 0.05
    for i in range(1, n):
        theta[i] = np.random.normal(theta[i-s], sd)
        phi[i] = np.random.normal(phi[i-s], sd)
        x[i] = x[i-s]+ds*np.sin(theta[i-s])*np.cos(phi[i-s])
        y[i] = y[i-s]+ds*np.sin(theta[i-s])*np.sin(phi[i-s])
        z[i] = z[i-s]+ds*np.cos(theta[i-s])

    return x, y, z


def alg_myon_trace(vmf: Vmf):
    # cfg
    block_xr = 64
    block_yr = 64
    block_zr = 16
    r = 20
    for i in range(r):
        x, y, z = little_test(6969)
        if plot:
            plt.plot(z, x)
        if gen:
            for j in range(len(x)):
                # TODO add z var (or keep static (?))
                # TODO add blockdiff range
                print(str(i)+"/"+str(r)+" :: " + str(j)+"/"+str(len(x)))
                vmf.add_solid(Vertex(x[j], z[j], 0),block_xr, block_yr, block_zr, checkCollisionType=2)

    if plot:
        plt.show()
