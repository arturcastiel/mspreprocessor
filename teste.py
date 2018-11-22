import msCoarseningLib.algoritmo as bib
import numpy as np

import msCoarseningLib.configManager as cp

p = np.array([1, 1, 1 , 3, 3,  9, 9, 0, 0 , 4 , 1 ,1 , 4, 6, 11, 12, 15, 3])


lo = cp.readConfig("msCoarse.ini")

print(p)
print(lo)