
import numpy as np
from meshHandle.multiscaleMesh import FineScaleMeshMS as msh
import time
import pdb
import geoUtil.geoTools as gtool

from math import pi, sqrt
from pymoab import core, types, rng, topo_util


# docker run -t -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"

# docker run -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"
# %load_ext autoreload
# %autoreload 2


start = time. time()
M = msh("malha-teste.h5m", dim = 3)
vec = np.arange(len(M.alma)).astype(int)
# M.core.print()
end = time. time()
print("Execution time for a {2}d mesh with {0} elements: {1} seconds".format(len(M), end-start, M.dim ))


start = time. time()
#M.core.print()
end = time. time()
print("Printing Routine Time: {}".format(end-start))


start = time. time()
M.core.print()
end = time. time()
print("Printing Routine Time: {}".format(end-start))


# start = time. time()
# M.faces.normal[:]
# end = time. time()
# print("Printing Routine Time: {}".format(end-start))


# vec2 = np.array([vec,vec,vec]).T
# #M.alma.set_data(vec2)
# M.alma[:] = vec2
# vec3 = np.array([10,12,13,14,30,35])
#
# vec1 = np.arange(8)
# p = vec2[2:10,:]
#
#
#
# M.core.print()


# cumaru = M.core.mb.tag_get_handle("GEOM_DIMENSION")
# M.core.handleDic["GEOM_DIMENSION"] = cumaru
#
#
#
#
# loook = M.core.mb.get_entities_by_type_and_tag(
#     0, types.MBENTITYSET, np.array(
#         (cumaru,)), np.array((None,)))
