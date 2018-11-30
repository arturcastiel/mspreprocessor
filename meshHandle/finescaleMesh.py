
import time
import pdb
import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util
from . corePymoab import CoreMoab

print('STANDARD FINESCALE MESH - NO MULTISCALE')
class FineScaleMesh:
    def __init__(self,mesh_file, dim=3):
        self.core = CoreMoab(mesh_file)
        self.init_Center()
        self.init_Volume()
        self.init_Normal()
        self.macroDim()
        self.init_ID()
        #self.init_BC()
        # Iniciar condições de contorno
        self.dirichlet_faces = set()
        self.neumann_faces = set()

    def macroDim(self):
        coords = self.core.mb.get_coords(self.core.all_nodes).reshape(len(self.core.all_nodes),3)
        self.rx = (coords[:,0].min(), coords[:,0].max())
        self.ry = (coords[:,1].min(), coords[:,1].max())
        self.rz = (coords[:,2].min(), coords[:,2].max())

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

    def init_bc(self):
        print("Inicializando BC")
        physical_tag = self.core.mb.tag_get_handle("MATERIAL_SET")
        dirchlet_tag = self.core.mb.tag_get_handle("DIRICHLET_SET")
        neumamn_tag = self.core.mb.tag_get_handle("NEUMANN_SET")
        physical_sets = self.core.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (physical_tag,)), np.array((None,)))

        dirichtlet_sets = self.core.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (dirchlet_tag,)), np.array((None,)))

        neumamn_sets = self.core.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (neumamn_tag,)), np.array((None,)))

        print(dirichtlet_sets)
        print(neumamn_sets)
        print(physical_sets)

        #bunda_tag = self.core.mb.tag_get_handle("BUNDA")

        self.core.handleDic["MATERIAL_SET"] = physical_tag
        self.core.handleDic["DIRICHLET_SET"] = dirchlet_tag

        self.core.handleDic["NEUMANN_SET"] = neumamn_tag
        #self.core.handleDic["BUNDA"] = bunda_tag
        pdb.set_trace()
        print(physical_tag)
        print(dirchlet_tag)
        print(neumamn_tag)


    def init_ID(self):
        # delete previous IDs
        # Gmesh standard counts from 1
        GLOBAL_ID_tag = self.core.mb.tag_get_handle(
            "Global_ID", 1, types.MB_TYPE_INTEGER, types.MB_TAG_DENSE, True)
        self.core.mb.tag_delete(GLOBAL_ID_tag)

        self.core.deftagHandle("GLOBAL_ID",1, dataText = 'int')
        #create volume ids
        self.core.setData("GLOBAL_ID", np.arange(len(self.core.all_volumes)))
        #create face ids
        self.core.setData("GLOBAL_ID", np.arange(len(self.core.all_faces)),rangeEl = self.core.all_faces)
        #create edges ids
        self.core.setData("GLOBAL_ID", np.arange(len(self.core.all_edges)),rangeEl = self.core.all_edges)
        #create nodes ids
        self.core.setData("GLOBAL_ID", np.arange(len(self.core.all_nodes)),rangeEl = self.core.all_nodes)

    def init_Center(self):
        self.core.deftagHandle('CENTER',3)
        #centro dos volumes
        centers = np.zeros((len(self.core.all_volumes),3)).astype('float')
        index = 0
        for volume in self.core.all_volumes:
            centers[index] = self.get_centroid(volume)
            index += 1
        self.core.setData("CENTER",centers)
        #centro das faces
        centers = np.zeros((len(self.core.all_faces), 3)).astype('float')
        index = 0
        for face in self.core.all_faces:
            centers[index] = self.get_centroid(face)
            index += 1
        self.core.setData("CENTER", centers, rangeEl = self.core.all_faces)

        #centro das arestas
        centers = np.zeros((len(self.core.all_edges), 3)).astype('float')
        index = 0
        for edge in self.core.all_edges:
            centers[index] = self.get_centroid(edge)
            index += 1
        self.core.setData("CENTER", centers, rangeEl = self.core.all_edges)

    def init_Normal(self):
        self.core.deftagHandle('NORMAL', 3)
        normal = np.zeros((len(self.core.all_faces), 3)).astype('float')
        index = 0
        for face in self.core.all_faces:
            verts = self.core.mb.get_connectivity(face)
            coords = np.array([self.core.mb.get_coords([vert]) for vert in verts])
            vec1 = coords[1] - coords[0]
            vec2 = coords[2] - coords[0]
            cross = np.cross(vec1,vec2)
            normal[index] = cross/np.linalg.norm(cross)
            index += 1
        self.core.setData("NORMAL", normal, rangeEl=self.core.all_faces)


    def init_Volume(self):
        mat = np.zeros(self.core.all_volumes.size())
        index = 0
        for vol in  self.core.all_volumes:
            mat[index] = self.get_volume(vol)
            index += 1
        self.core.deftagHandle("VOLUME",1)
        #pdb.set_trace()
        self.core.setData("VOLUME",mat)
        #volTag = self.mb.tag_get_handle("VOLUME", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_DENSE, True)
        #self.mb.tag_set_data(volTag, self.all_volumes, mat)
        #return volTag

    def get_centroid(self, entity):
        verts = self.core.mb.get_connectivity(entity)
        coords = np.array([self.core.mb.get_coords([vert]) for vert in verts])
        qtd_pts = len(verts)
        #print qtd_pts, 'qtd_pts'
        coords = np.reshape(coords, (qtd_pts, 3))
        pseudo_cent = sum(coords)/qtd_pts
        return pseudo_cent

    def get_volume(self,entity):
        #input: entity tag
        #ouput: volume of a entity
        verts = self.core.mb.get_connectivity(entity)
        coords = np.array([self.core.mb.get_coords([vert]) for vert in verts])
        qtd_pts = len(verts)
        if qtd_pts == 4:
            pass
            vect_1 = coords[1] - coords[0]
            vect_2 = coords[2] - coords[0]
            vect_3 = coords[3] - coords[0]
            vol_eval = abs(np.dot(np.cross(vect_1, vect_2), vect_3)) / 6.0
        elif qtd_pts == 8:
            pass
            #SEGUNDA ATIVIDADE PRA RENATINHA
            #CALCULAR O VOLUME DO HEXAEDRO IERREGULAR DADO OS 8 PONTOS

            # pass
            # #pdb.set_trace()
            # vect_1 = coords[7] - coords[0]
            # vect_2 = coords[1] - coords[0]
            # vect_3 = coords[3] - coords[5]
            # vect_4 = coords[4] - coords[6]
            # vect_5 = coords[5] - coords[0]
            # vect_6 = coords[2] - coords[0]
            # vect_7 = coords[6] - coords[3]
            # D1 = np.linalg.det(np.array([vect_1, vect_2, vect_3]))
            # D2 = np.linalg.det(np.array([vect_1, vect_4, vect_5]))
            # D3 = np.linalg.det(np.array([vect_1, vect_6, vect_7]))
            # vol_eval = ((D1+D2+D3)/2)
            vol_eval = 1
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

    def get_piram_volume(self,tet_nodes):
        #PRIMEIRA ATIVIDADE PARA RENATINHA
        # atividade para renata
        #input: 5 handles para os 5 nós da piramide
        #output: volume da piramide

        #ler biblioteca do numpy para isso
        #metodo get_tetravolume como base
        pass

    @staticmethod
    def point_distance(coords_1, coords_2):
        dist_vector = coords_1 - coords_2
        distance = sqrt(np.dot(dist_vector, dist_vector))
        return distance


#--------------Início dos parâmetros de entrada-------------------
