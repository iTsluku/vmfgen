from model.Vmf import Vmf
from model.Vertex import Vertex
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def alg_shape_3d(vmf: Vmf):
    # cfg
    addSolid = True
    draw = False

    block_xr = 96
    block_yr = 96
    block_zr = 128
    assert block_xr == block_yr
    dimRange = 8192
    blockDiffRange = 48
    #s1 = 0.01
    #s2 = 0.01
    numberPoints = int(dimRange/(block_xr+blockDiffRange))
    assert numberPoints > 0

    X = np.linspace(0, dimRange, numberPoints)
    Y = np.linspace(0, dimRange, numberPoints)
    xx, yy = np.meshgrid(X, Y)
    # todo outsource func
    # todo try p60 numpy doc
    zz = 192*np.cos((0.0008*xx)**2+8*np.cos(0.0009*yy)**2)
    #zz = (s1*(xx))**2-(s2*(yy))**2
    points = np.vstack((xx.flatten(), yy.flatten(), zz.flatten())).T

    if draw:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, cmap='viridis')
        plt.show()

    if addSolid:
        i = 1
        for p in points:
            assert len(p) == 3
            pX = int(p[0])
            pY = int(p[1])
            pZ = int(p[2])

            if pX % 2 != 0:
                pX = pX + 1
            if pY % 2 != 0:
                pY = pY + 1
            if pZ % 2 != 0:
                pZ = pZ + 1

            vmf.add_solid(Vertex(pX, pY, pZ), block_xr, block_yr, block_zr)
            # debug
            print(str(i)+" / "+str(len(points)))
            i += 1
            #print(pX, pY, pZ)
