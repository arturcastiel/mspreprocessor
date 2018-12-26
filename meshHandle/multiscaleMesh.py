
import time
import pdb
import configparser as cp
from . finescaleMesh import FineScaleMesh
import msCoarseningLib.algoritmo
#from msCoarseningLib.configManager import readConfig

import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util


print('Initializing Finescale Mesh for Multiscale Methods')
class FineScaleMeshMS(FineScaleMesh):
    def __init__(self,mesh_file, dim=3):
        super().__init__(mesh_file,dim)

        #self.init_partition()

    def init_partition(self):
        config = self.read_config()
        particionador_type = config.get("Particionador","algoritmo")
        print(particionador_type)
        if particionador_type != '0':
            name_function = "scheme" + particionador_type
            key = "Coarsening_" + particionador_type + "_Input"
            specific_attributes = config.items(key)
            used_attributes = []
            for at in specific_attributes:
                used_attributes.append(float(at[1]))
            used_attributes = [int(el) for el in used_attributes]
            part_tag = getattr(msCoarseningLib.algoritmo, name_function)(self.core.read_data("CENTER"),
                       len(self.core.all_faces), self.rx, self.ry, self.rz,*used_attributes)
            self.core.create_tag_handle("PARTITION", 1, data_text="int")
            self.core.set_data("PARTITION",part_tag[0])

    def read_config(self, config_input="msCoarse.ini"):
        config_file = cp.ConfigParser()
        config_file.read(config_input)
        return config_file
