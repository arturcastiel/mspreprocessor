
import numpy as np
from meshHandle.multiscaleMesh import FineScaleMeshMS as msh
import pdb

from math import pi, sqrt
from pymoab import core, types, rng, topo_util


#docker run -t -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"

#docker run -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"
#%load_ext autoreload
#%autoreload 2



M = msh("semi.msh")

# M.core.readData("DIRICHLET", rangeEl = M.core.all_nodes)
#pdb.set_trace()
# print(M.core.access_meshset(0))
# print(M.core.mb.get_entities_by_handle(0))
M.core.print()

vec = np.array([0,1,2,3,4])
vec2 = np.zeros(len(M.core.all_faces),dtype = bool)

vec2[0] = True

vec2[10] = True
l = M.core.filter_range(M.core.all_faces, vec2)

print("----------------------------------")


#M.core.check_handle_dimension(M.core.all_volumes)
#
p = M.core.range_merge(M.core.all_edges, M.core.all_faces, M.core.all_volumes, M.core.all_nodes)

print(p)

print("----------------------------------")

print(M.core.filter_handle_by_dimension(p,0,2,3))


# print(M.core.readData("GLOBAL_ID", rangeEl = M.core.all_faces))
#
# print(M.core.readData("GLOBAL_ID", rangeEl = M.core.all_edges))
#
# print(M.core.readData("GLOBAL_ID", rangeEl = M.core.all_nodes))
#
# print(M.core.readData("GLOBAL_ID", rangeEl = M.core.all_volumes))







# cumaru = M.core.mb.tag_get_handle("GEOM_DIMENSION")
# M.core.handleDic["GEOM_DIMENSION"] = cumaru
#
#
#
#
# loook = M.core.mb.get_entities_by_type_and_tag(
#     0, types.MBENTITYSET, np.array(
#         (cumaru,)), np.array((None,)))