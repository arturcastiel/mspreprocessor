
import time
import pdb

from . finescaleMesh import FineScaleMesh

import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util


print('FINESCALE WITH MULTISCALE')
class FineScaleMeshMS(FineScaleMesh):
    def __init__(self,mesh_file, dim=3):
        print(mesh_file + 'entrou')
        super().__init__(mesh_file,dim)
        self.macroDim()
        # self.dimension = dim
        # self.mb = core.Core()
        # self.root_set = self.mb.get_root_set()
        # self.mtu = topo_util.MeshTopoUtil(self.mb)
        # self.mb.load_file(mesh_file)
        #
        # # self.tagDic- dicionário de tag
        # # input: string do tag
        # # output: pymoab Tag


        # self.handleDic = {}
        # self.physical_tag = self.mb.tag_get_handle("MATERIAL_SET")
        # self.handleDic['MATERIAL_SET'] = self.physical_tag
        # self.physical_sets = self.mb.get_entities_by_type_and_tag(
        #     0, types.MBENTITYSET, np.array(
        #     (self.physical_tag,)), np.array((None,)))
        # self.dirichlet_tag = self.mb.tag_get_handle(
        #     "Dirichlet", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        # self.neumann_tag = self.mb.tag_get_handle(
        #     "Neumann", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        # self.perm_tag = self.mb.tag_get_handle(
        #     "Permeability", 9, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        # self.source_tag = self.mb.tag_get_handle(
        #     "Source term", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        # self.all_volumes = self.mb.get_entities_by_dimension(0, self.dimension)
        # self.all_nodes = self.mb.get_entities_by_dimension(0, 0)
        # self.mtu.construct_aentities(self.all_nodes)
        # self.all_faces = self.mb.get_entities_by_dimension(0, self.dimension-1)
        # self.all_edges = self.mb.get_entities_by_dimension(0, self.dimension-2)
        # self.init_Center()
        # self.init_Volume()
        # self.init_Normal()
        # self.macroDim()
        # self.dirichlet_faces = set()
        # self.neumann_faces = set()
    def macroDim(self):
        coords = self.mb.get_coords(self.all_nodes).reshape(len(self.all_nodes),3)
        self.rx = (coords[:,0].min(), coords[:,0].max())
        self.ry = (coords[:,1].min(), coords[:,1].max())
        self.rz = (coords[:,2].min(), coords[:,2].max())


#--------------Início dos parâmetros de entrada-------------------
