
import time
import pdb
import configparser as cp
from . finescaleMesh import FineScaleMesh
import msCoarseningLib.algoritmo
#from msCoarseningLib.configManager import readConfig
from . meshComponents import MoabVariable, MeshEntities
from . mscorePymoab import MsCoreMoab

from . meshComponentsMS import MultiscaleMeshEntities ,MoabVariableMS,  MeshEntitiesMS


import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util


print('Initializing Finescale Mesh for Multiscale Methods')


class FineScaleMeshMS(FineScaleMesh):
    def __init__(self,mesh_file, dim=3):
        super().__init__(mesh_file,dim)
        self.partition = self.init_partition()
        self.coarse_volumes = [CoarseVolume(self.core, self.dim, i, self.partition[:] == i) for i in range(self.partition[:].max()+1 )]
        self.general = MultiscaleMeshEntities(self.core,self.coarse_volumes)
        for i,el in zip(range(len(self.coarse_volumes)),self.coarse_volumes):
            el(i,self.general)

    def init_entities(self):
        self.nodes = MeshEntitiesMS(self.core, entity_type = "node")
        self.edges = MeshEntitiesMS(self.core, entity_type = "edges")
        self.faces = MeshEntitiesMS(self.core, entity_type = "faces")
        if self.dim == 3:
            self.volumes = MeshEntitiesMS(self.core, entity_type = "volumes")


    def init_variables(self):
        self.alma = MoabVariableMS(self.core,data_size=1,var_type= "volumes",  data_format="int", name_tag="alma")
        self.ama = MoabVariableMS(self.core,data_size=1,var_type= "faces",  data_format="float", name_tag="ama",data_density="sparse")
        self.arma = MoabVariableMS(self.core,data_size=3,var_type= "edges",  data_format="float", name_tag="arma",
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

        self.init_entities()
        self.init_variables()
        self.init_coarse_variables()
        self.macro_dim()

    def init_variables(self):
        pass

    def __call__(self,i,general):
        self.nodes.enhance(i,general)
        self.edges.enhance(i,general)
        self.faces.enhance(i,general)
        if self.dim == 3:
            self.volumes.enhance(i,general)

        pass

    def init_coarse_variables(self):
        self.lama = MoabVariableMS(self.core,data_size=1,var_type= "faces",  data_format="int", name_tag="lama", level=self.level, coarse_num=self.coarse_num)
