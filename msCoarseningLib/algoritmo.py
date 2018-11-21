
import pdb
from . import readConfig

def scheme1(msh):
    # msh -> objeto da clase meshUtil
    centerCoord = msh.readData("CENTER")
    print(centerCoord)
    pdb.set_trace()

    op  = readConfig.readConfig()
    checkinBox(centerCoord)






def checkinBox(coords, x = (1,2), y = (2,3), z = (3,4)):
    tag1 = (coords[:,0] > x[0])   &  (coords[:,0] < x[1])
    tag2 = (coords[:,1] > y[0])   &  (coords[:,1] < y[1])
    tag3 = (coords[:,2] > z[0])   &  (coords[:,2] < z[1])
    return tag1 & tag2 & tag3
