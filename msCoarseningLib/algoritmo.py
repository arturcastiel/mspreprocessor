
import pdb
import numpy as np
import pdb
def scheme1(centerCoord, num_of_vol, rx,ry,rz ,nx = 3, ny = 3, nz =3 ):
    #input : centerCoord - > array with the center of elements
    #        num_of_vol = number of volumes
    #        rx,ry,rz - (min, max) values of x,y,z
    #        nx, ny, nz

    # msh -> objeto da clase meshUtil
    #centerCoord = msh.readData("CENTER")

    box = np.array([0, (rx[1] - rx[0])/nx, 0,(ry[1] - ry[0]) /ny, 0,(rz[1] - rz[0])/(nz+0)]).reshape(3,2)
    cent_coord_El1 = box.sum(axis =1)/2
    tag = np.zeros(num_of_vol).astype("int")
    index = 0
    for x in range(nx):
        for y in range(ny):
            for z in range(nz):
                inc = np.multiply(box[:,1], np.array([x,y,z]))
                cent = cent_coord_El1 + inc
                #inc = np.array([(nx) * x, (ny) * y, (nz) * z])
                boxMin = box[:,0] + inc
                boxMax = box[:,1] + inc
                point = checkinBox(centerCoord,x=(boxMin[0], boxMax[0]), y=(boxMin[1], boxMax[1]) , z=(boxMin[2], boxMax[2]))
                tag[point] = index
                index += 1
    tagAdjust(tag)
    return tag


def tagAdjust(tag):
    # msh -> objeto da clase meshUtil
    min = tag.min()
    max = tag.max()


    pdb.set_trace()

def checkinBox(coords, x = (1,2), y = (2,3), z = (3,4)):
    tag1 = (coords[:,0] > x[0])   &  (coords[:,0] < x[1])
    tag2 = (coords[:,1] > y[0])   &  (coords[:,1] < y[1])
    tag3 = (coords[:,2] > z[0])   &  (coords[:,2] < z[1])
    return tag1 & tag2 & tag3
