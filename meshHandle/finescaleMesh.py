import time
import pdb
import numpy as np
from math import pi, sqrt
from pymoab import core, types, rng, topo_util
from . corePymoab import CoreMoab
from . meshComponents import MoabVariable, MeshEntities


print('Standard fine-scale mesh loaded: No multiscale components available')
class FineScaleMesh:
    def __init__(self,mesh_file, dim=3):
        self.core = CoreMoab(mesh_file)
        self.alma = MoabVariable(self.core,data_size=1,var_type= "volumes",  data_format="int", name_tag="alma")

        self.nodes = MeshEntities(self.core, entity_type = "node")

        self.edges = MeshEntities(self.core, entity_type="edges")

        self.faces = MeshEntities(self.core, entity_type = "faces")

        self.volumes = MeshEntities(self.core, entity_type = "volumes")

        self.ama = MoabVariable(self.core,data_size=1,var_type= "faces",  data_format="float", name_tag="ama",
                                entity_index= self.faces.boundary, data_density="dense")

        self.arma = MoabVariable(self.core,data_size=3,var_type= "nodes",  data_format="float", name_tag="arma",
                                 data_density="sparse")
        #pdb.set_trace()

        self.init_center()
        self.init_volume()
        self.init_normal()
        self.macro_dim()

        #self.init_BC()
        # Iniciar condições de contorno
        self.dirichlet_faces = set()
        self.neumann_faces = set()

    def macro_dim(self):
        coords = self.core.mb.get_coords(self.core.all_nodes).reshape(len(self.core.all_nodes),3)
        self.rx = (coords[:,0].min(), coords[:,0].max())
        self.ry = (coords[:,1].min(), coords[:,1].max())
        self.rz = (coords[:,2].min(), coords[:,2].max())


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
        #pdb.set_trace()
        print(physical_tag)
        print(dirchlet_tag)
        print(neumamn_tag)



    def init_center(self):
        self.core.create_tag_handle('CENTER',3)
        #centro dos volumes
        centers = np.zeros((len(self.core.all_volumes),3)).astype('float')
        index = 0
        for volume in self.core.all_volumes:
            centers[index] = self.get_centroid(volume)
            index += 1
        self.core.set_data("CENTER",centers)
        #centro das faces
        centers = np.zeros((len(self.core.all_faces), 3)).astype('float')
        index = 0
        for face in self.core.all_faces:
            centers[index] = self.get_centroid(face)
            index += 1
        self.core.set_data("CENTER", centers, range_el = self.core.all_faces)

        #centro das arestas
        centers = np.zeros((len(self.core.all_edges), 3)).astype('float')
        index = 0
        for edge in self.core.all_edges:
            centers[index] = self.get_centroid(edge)
            index += 1
        self.core.set_data("CENTER", centers, range_el = self.core.all_edges)

    def init_normal(self):
        self.core.create_tag_handle('NORMAL', 3)
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
        self.core.set_data("NORMAL", normal, range_el=self.core.all_faces)


    def init_volume(self):
        mat = np.zeros(self.core.all_volumes.size())
        index = 0
        for vol in  self.core.all_volumes:
            mat[index] = self.get_volume(vol)
            index += 1
        self.core.create_tag_handle("VOLUME",1)
        #pdb.set_trace()
        self.core.set_data("VOLUME",mat)
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
