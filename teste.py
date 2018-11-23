
import numpy as np
from meshHandle.multiscaleMesh import FineScaleMeshMS as msh3
from  meshHandle.corePymoab import CoreMoab

p = np.array([1, 1, 1 , 3, 3,  9, 9, 0, 0 , 4 , 1 ,1 , 4, 6, 11, 12, 15, 3])
M = msh3("8.msh")



#CM = CoreMoab(M.all_nodes, M.all_edges, M.all_faces, M.all_volumes)