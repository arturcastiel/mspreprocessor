
import numpy as np
from meshHandle.multiscaleMesh import FineScaleMeshMS as msh

import pdb

from math import pi, sqrt
from pymoab import core, types, rng, topo_util


# docker run -t -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"

# docker run -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"
# %load_ext autoreload
# %autoreload 2



M = msh("semi.msh")
vec = np.arange(len(M.alma)).astype(int)

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
