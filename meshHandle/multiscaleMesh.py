
import time
import pdb
import configparser as cp
from . finescaleMesh import FineScaleMesh
import msCoarseningLib.algoritmo
#from msCoarseningLib.configManager import readConfig
from . meshComponents import MoabVariable, MeshEntities
from . mscorePymoab import MsCoreMoab

from . meshComponentsMS import MultiscaleMeshEntities ,MoabVariableMS


import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util


print('Initializing Finescale Mesh for Multiscale Methods')


class FineScaleMeshMS(FineScaleMesh):
    def __init__(self,mesh_file, dim=3):
        super().__init__(mesh_file,dim)
        self.partition = self.init_partition()
        self.coarse_volumes = [CoarseVolume(self.core, self.dim, i, self.partition[:] == i) for i in range(self.partition[:].max())]
        self.general = MultiscaleMeshEntities(self.core,self.coarse_volumes)

    def init_variables(self):
        self.alma = MoabVariable(self.core,data_size=1,var_type= "volumes",  data_format="int", name_tag="alma")
        self.ama = MoabVariable(self.core,data_size=1,var_type= "faces",  data_format="float", name_tag="ama",
                                entity_index= self.faces.boundary, data_density="dense")
        self.arma = MoabVariable(self.core,data_size=3,var_type= "edges",  data_format="float", name_tag="arma",
                                 data_density="sparse")


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


    def init_partition_parallel(self):
        if self.dim == 3:
            partition = MoabVariable(self.core,data_size=1,var_type= "volumes",  data_format="int", name_tag="Parallel",
                                         data_density="sparse")

            # partition[:]
            # [partition[:],coarse_center]  = getattr(msCoarseningLib.algoritmo, name_function)(self.volumes.center[:],
            #            len(self), self.rx, self.ry, self.rz,*used_attributes)
        elif self.dim == 2:
            partition = MoabVariable(self.core,data_size=1,var_type= "faces",  data_format="int", name_tag="Parallel",
                                         data_density="sparse")
        return partition

    def read_config(self, config_input="msCoarse.ini"):
        config_file = cp.ConfigParser()
        config_file.read(config_input)
        return config_file


class CoarseVolume(FineScaleMeshMS):
    def __init__(self, father_core, dim, i, coarse_vec):
        self.dim = dim
        self.level = father_core.level + 1
        self.coarse_num = i

        print("Level {0} - Volume {1}".format(self.level,self.coarse_num))

        self.core = MsCoreMoab(father_core, i, coarse_vec)
        # print(self.core.level)

        self.init_entities()
        self.init_variables()
        self.init_coarse_variables()
        self.macro_dim()

    def init_coarse_variables(self):
        self.lama = MoabVariableMS(self.core,data_size=1,var_type= "volumes",  data_format="int", name_tag="lama", level=self.level, coarse_num=self.coarse_num)
