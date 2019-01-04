
import time
import pdb
import configparser as cp
from . finescaleMesh import FineScaleMesh
import msCoarseningLib.algoritmo
#from msCoarseningLib.configManager import readConfig
from . meshComponents import MoabVariable, MeshEntities
from . mscorePymoab import MsCoreMoab



import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util


print('Initializing Finescale Mesh for Multiscale Methods')
class CoarseVolume(FineScaleMesh):
    def __init__(self, father_core, dim, coarse_vec ):
        self.dim = dim
        self.core = MsCoreMoab(father_core, coarse_vec)
        print(self.core.level)

        self.init_entities()
        print('successfully')
    pass

class FineScaleMeshMS(FineScaleMesh):
    def __init__(self,mesh_file, dim=3):
        super().__init__(mesh_file,dim)


        self.partition = self.init_partition()
        # self.a = MsCoreMoab(self.core, self.partition[:] == 5)

        self.coarse_volumes = CoarseVolume(self.core, self.dim, self.partition[:] == 5)
        #self.b = MsCoreMoab(self.core, self.partition[:] == 5)


    def init_partition(self):
        config = self.read_config()
        particionador_type = config.get("Particionador","algoritmo")
        if particionador_type != '0':
            if self.dim == 3:
                partition = MoabVariable(self.core,data_size=1,var_type= "volumes",  data_format="int", name_tag="Partition",
                                             data_density="sparse")
                name_function = "scheme" + particionador_type
                key = "Coarsening_" + particionador_type + "_Input"
                specific_attributes = config.items(key)
                used_attributes = []
                for at in specific_attributes:
                    used_attributes.append(float(at[1]))
                [partition[:],coarse_center]  = getattr(msCoarseningLib.algoritmo, name_function)(self.volumes.center[:],
                           len(self), self.rx, self.ry, self.rz,*used_attributes)
            elif self.dim == 2:
                partition = MoabVariable(self.core,data_size=1,var_type= "faces",  data_format="int", name_tag="Partition",
                                             data_density="sparse")
                name_function = "scheme" + particionador_type
                key = "Coarsening_" + particionador_type + "_Input"
                specific_attributes = config.items(key)
                used_attributes = []
                for at in specific_attributes:
                    used_attributes.append(float(at[1]))
                [partition[:],coarse_center]  = getattr(msCoarseningLib.algoritmo, name_function)(self.faces.center[:],
                           len(self), self.rx, self.ry, self.rz,*used_attributes)
            return partition

    def read_config(self, config_input="msCoarse.ini"):
        config_file = cp.ConfigParser()
        config_file.read(config_input)
        return config_file
