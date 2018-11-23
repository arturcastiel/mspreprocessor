
import numpy as np
from meshHandle.multiscaleMesh import FineScaleMeshMS as msh3
# import numpy as np
#
# import pdb
# import msCoarseningLib.algoritmo

#docker run -t -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"

#docker run -it -v  /home/arturcastiel/projetos:/pytest desenvolvimento:latest bash -c "cd /pytest; bash"
#%load_ext autoreload
#%autoreload 2

#M1 = msh('8.msh')

#M2 = msh2("8.msh")


M3 = msh3("8.msh")


# vec = np.arange(len(M3.core.all_volumes)).astype(int)
# tf = np.array([True, False])
#
# a = np.random.choice(tf, int(2311))
#
#
#
# vec2 = vec[1:30]
# vec3 = np.array([1,3,4,2,5,2],dtype = 'uint')

#rangeMod = M1.rangeIndex(vec2)
# data = np.roll(vec2,3)
#op = ai.readConfig()


# point = np.arange(len(M3.core.all_nodes)).astype("int")
#
# # lep = msCoarseningLib.algoritmo.scheme1(M3)
# #
# # M3.deftagHandle("PARTITION",1, dataText="int")
# # M3.setData("PARTITION",lep)

#M3.core.print()

