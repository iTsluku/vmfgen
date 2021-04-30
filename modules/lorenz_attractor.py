from model.Vmf import Vmf
from model.Vertex import Vertex
import numpy as np
from scipy.integrate import odeint


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

    # todo add import
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
