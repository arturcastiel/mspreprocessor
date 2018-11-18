
import time
import pdb
import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util
print('MeshManager class loadded')
class MeshManager:
    def __init__(self,mesh_file, dim=3):
        self.dimension = dim
        self.mb = core.Core()
        self.root_set = self.mb.get_root_set()
        self.mtu = topo_util.MeshTopoUtil(self.mb)
        self.mb.load_file(mesh_file)

        # self.tagDic- dicionário de tag
        # input: string do tag
        # output: pymoab Tag
        self.handleDic = {}
        self.physical_tag = self.mb.tag_get_handle("MATERIAL_SET")
        self.handleDic['MATERIAL_SET'] = self.physical_tag
        """
        #
        #self.tagDic['MATERIAL_SET'] = self.physical_tag    
        """
        self.physical_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (self.physical_tag,)), np.array((None,)))

        #print(self.physical_sets)
        self.dirichlet_tag = self.mb.tag_get_handle(
            "Dirichlet", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        self.neumann_tag = self.mb.tag_get_handle(
            "Neumann", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        self.perm_tag = self.mb.tag_get_handle(
            "Permeability", 9, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        self.source_tag = self.mb.tag_get_handle(
            "Source term", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)
        self.all_volumes = self.mb.get_entities_by_dimension(0, self.dimension)

        self.init_Volume()

        self.all_nodes = self.mb.get_entities_by_dimension(0, 0)
        self.mtu.construct_aentities(self.all_nodes)
        self.all_faces = self.mb.get_entities_by_dimension(0, self.dimension-1)

        self.dirichlet_faces = set()
        self.neumann_faces = set()

        '''self.GLOBAL_ID_tag = self.mb.tag_get_handle(
            "Global_ID", 1, types.MB_TYPE_INTEGER, types.MB_TAG_DENSE, True)'''
    def deftagHandle(self,nameTag,dataSize, dataText = "float", dataDensity = types.MB_TAG_DENSE ):
         if dataText == 'float':
             dataType = types.MB_TYPE_DOUBLE
         elif dataText == "int":
             dataType = types.MB_TYPE_INTEGER
         elif dataText == "bool":
             dataType == types.MB_TYPE_BIT
         try:
             handle = self.handleDic[nameTag]
         except KeyError:
             handle = self.mb.tag_get_handle(nameTag, dataSize, dataType, dataDensity, True)
             self.handleDic[nameTag] = handle

    def readData(self, nametag, indexVec = np.array([]), rangeEl = None):
         if rangeEl == None:
             rangeEl = self.all_volumes
         if indexVec.size > 0:
             rangeEl = self.rangeIndex(indexVec,rangeEl)
         try:
            handleTag = self.handleDic[nametag]
            return self.mb.tag_get_data(handleTag, rangeEl)
         except KeyError:
             print("Tag não encontrado")

    def rangeIndex(self, vecIndex, rangeHandle = None):
        if rangeHandle == None:
             rangeHandle = self.all_volumes
        if vecIndex.dtype == "bool":
            vec = np.where(vecIndex)[0]
        else:
            vec = vecIndex.astype("uint")
        handles = np.asarray(rangeHandle)[vec.astype("uint")].astype("uint")
        return rng.Range(handles)


    def setData(self, nametag,data, indexVec = np.array([]), rangeEl = None):
         if rangeEl == None:
             rangeEl = self.all_volumes
         if indexVec.size > 0:
             rangeEl = self.rangeIndex(indexVec,rangeEl)
         handleTag = self.handleDic[nametag]
         self.mb.tag_set_data(handleTag,rangeEl,data)

    def create_vertices(self, coords):
        new_vertices = self.mb.create_vertices(coords)
        self.all_nodes.append(new_vertices)
        return new_vertices

    def create_element(self, poly_type, vertices):
        new_volume = self.mb.create_element(poly_type, vertices)
        self.all_volumes.append(new_volume)
        return new_volume

    def set_information(self, information_name, physicals_values,
                        dim_target, set_connect=False):

        information_tag = self.mb.tag_get_handle(information_name)
        for physical, value in physicals_values.items():
            for a_set in self.physical_sets:
                physical_group = self.mb.tag_get_data(self.physical_tag,
                                                      a_set, flat=True)

                if physical_group == physical:
                    group_elements = self.mb.get_entities_by_dimension(a_set, dim_target)

                    if information_name == 'Dirichlet':
                        # print('DIR GROUP', len(group_elements), group_elements)
                        self.dirichlet_faces = self.dirichlet_faces | set(
                                                    group_elements)

                    if information_name == 'Neumann':
                        # print('NEU GROUP', len(group_elements), group_elements)
                        self.neumann_faces = self.neumann_faces | set(
                                                  group_elements)

                    for element in group_elements:
                        self.mb.tag_set_data(information_tag, element, value)

                        if set_connect:
                            connectivities = self.mtu.get_bridge_adjacencies(
                                                                element, 0, 0)
                            self.mb.tag_set_data(
                                information_tag, connectivities,
                                np.repeat(value, len(connectivities)))

    def get_boundary_nodes(self):
        all_faces = self.dirichlet_faces | self.neumann_faces
        boundary_nodes = set()
        for face in all_faces:
            nodes = self.mtu.get_bridge_adjacencies(face, 2, 0)
            boundary_nodes.update(nodes)
        return boundary_nodes

    def get_non_boundary_volumes(self, dirichlet_nodes, neumann_nodes):
        volumes = self.all_volumes
        non_boundary_volumes = []
        for volume in volumes:
            volume_nodes = set(self.mtu.get_bridge_adjacencies(volume, 0, 0))
            if (volume_nodes.intersection(dirichlet_nodes | neumann_nodes)) == set():
                non_boundary_volumes.append(volume)

        return non_boundary_volumes

    def set_media_property(self, property_name, physicals_values,
                           dim_target=3, set_nodes=False):

        self.set_information(property_name, physicals_values,
                             dim_target, set_connect=set_nodes)

    def set_boundary_condition(self, boundary_condition, physicals_values,
                               dim_target=3, set_nodes=False):

        self.set_information(boundary_condition, physicals_values,
                             dim_target, set_connect=set_nodes)

    def init_Volume(self):
        mat = np.zeros(self.all_volumes.size())
        index = 0
        for vol in  self.all_volumes:
            mat[index] = self.get_volume(vol)
            index += 1
        self.deftagHandle("VOLUME",1)
        #pdb.set_trace()
        self.setData("VOLUME",mat)
        #volTag = self.mb.tag_get_handle("VOLUME", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_DENSE, True)
        #self.mb.tag_set_data(volTag, self.all_volumes, mat)
        #return volTag

    def get_centroid(self, entity):
        verts = self.mb.get_connectivity(entity)
        coords = np.array([self.mb.get_coords([vert]) for vert in verts])
        qtd_pts = len(verts)
        #print qtd_pts, 'qtd_pts'
        coords = np.reshape(coords, (qtd_pts, 3))
        pseudo_cent = sum(coords)/qtd_pts
        return pseudo_cent

    def get_volume(self,entity):
        #input: entity tag
        #ouput: volume of a entity
        verts = self.mb.get_connectivity(entity)
        coords = np.array([self.mb.get_coords([vert]) for vert in verts])
        qtd_pts = len(verts)
        if qtd_pts == 4:
            vect_1 = coords[1] - coords[0]
            vect_2 = coords[2] - coords[0]
            vect_3 = coords[3] - coords[0]
            vol_eval = abs(np.dot(np.cross(vect_1, vect_2), vect_3)) / 6.0
        elif qtd_pts == 8:
            #pdb.set_trace()
            vect_1 = coords[7] - coords[0]
            vect_2 = coords[1] - coords[0]
            vect_3 = coords[3] - coords[5]
            vect_4 = coords[4] - coords[6]
            vect_5 = coords[5] - coords[0]
            vect_6 = coords[2] - coords[0]
            vect_7 = coords[6] - coords[3]
            D1 = np.linalg.det(np.array([vect_1, vect_2, vect_3]))
            D2 = np.linalg.det(np.array([vect_1, vect_4, vect_5]))
            D3 = np.linalg.det(np.array([vect_1, vect_6, vect_7]))
            vol_eval = ((D1+D2+D3)/2)
            return vol_eval
        else:
            vol_eval  = 0
        return vol_eval

    def get_tetra_volume(self, tet_nodes):
        vect_1 = tet_nodes[1] - tet_nodes[0]
        vect_2 = tet_nodes[2] - tet_nodes[0]
        vect_3 = tet_nodes[3] - tet_nodes[0]
        vol_eval = abs(np.dot(np.cross(vect_1, vect_2), vect_3))/1
        return vol_eval

    @staticmethod
    def point_distance(coords_1, coords_2):
        dist_vector = coords_1 - coords_2
        distance = sqrt(np.dot(dist_vector, dist_vector))
        return distance


#--------------Início dos parâmetros de entrada-------------------