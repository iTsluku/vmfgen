import numpy as np


class Polar(object):
    def __init__(self, r: float, phi: float):
        self.r = r
        self.phi = phi % 2 * np.pi
        self.x = int(r * np.cos(np.degrees(phi)))
        self.y = int(r * np.sin(np.degrees(phi)))
