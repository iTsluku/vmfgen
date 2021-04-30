from model.Vmf import Vmf
import random
import numpy as np
from math import e
from sympy import prime
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
# import function
from modules.shape_3d import alg_shape_3d


# requires output.vmf file
def execute():
    vmf = Vmf()
    alg_shape_3d(vmf)
    f = open('output.vmf', 'r+')
    f.truncate(0)
    f.write(str(vmf))
    f.close()


# exec app
if __name__ == "__main__":
    execute()
