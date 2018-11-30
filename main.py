
import numpy as np
from meshHandle.multiscaleMesh import FineScaleMeshMS as msh
import pdb


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
