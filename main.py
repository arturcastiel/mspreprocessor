import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util
from pymoab import skinner as sk
import msCoarseningLib.readConfig
from meshUtil.meshManager import MeshManager as msh
import numpy as np
from msCoarseningLib import readConfig as ai
import pdb
import msCoarseningLib.algoritmo
#%load_ext autoreload
#%autoreload 2

M1 = msh('8.msh')


vec = np.arange(len(M1.all_volumes)).astype(int)
tf = np.array([True, False])
a = np.random.choice(tf, int(2311))

vec2 = vec[1:30]
vec3 = np.array([1,3,4,2,5,2],dtype = 'uint')

rangeMod = M1.rangeIndex(vec2)
data = np.roll(vec2,3)
op = ai.readConfig()


msCoarseningLib.algoritmo.scheme1(M1)



M1.print()
