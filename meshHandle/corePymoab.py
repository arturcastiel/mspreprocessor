from pymoab import core, types, rng, topo_util
import numpy as np
import pdb

class CoreMoab:
    def __init__(self,mesh_file, dim = 3):
        self.dimension = dim
        self.mb = core.Core()
        self.root_set = self.mb.get_root_set()
        self.mtu = topo_util.MeshTopoUtil(self.mb)
        self.mb.load_file(mesh_file)
        self.all_volumes = self.mb.get_entities_by_dimension(0, self.dimension)
        self.all_nodes = self.mb.get_entities_by_dimension(0, 0)
        self.mtu.construct_aentities(self.all_nodes)
        self.all_faces = self.mb.get_entities_by_dimension(0, self.dimension-1)
        self.all_edges = self.mb.get_entities_by_dimension(0, self.dimension-2)
        self.handleDic = {}
        self.read_bc()

    def read_bc(self):
        print("Inicializando BC")
        physical_tag = self.mb.tag_get_handle("MATERIAL_SET")
        dirchlet_tag = self.mb.tag_get_handle("DIRICHLET_SET")
        neumamn_tag = self.mb.tag_get_handle("NEUMANN_SET")
        physical_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (physical_tag,)), np.array((None,)))
        dirichtlet_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (dirchlet_tag,)), np.array((None,)))
        neumamn_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (neumamn_tag,)), np.array((None,)))


        print(dirichtlet_sets)
        print(neumamn_sets)
        print(physical_sets)

        #bunda_tag = self.core.mb.tag_get_handle("BUNDA")

        self.handleDic["MATERIAL_SET"] = physical_tag
        self.handleDic["DIRICHLET_SET"] = dirchlet_tag

        self.handleDic["NEUMANN_SET"] = neumamn_tag
        #self.core.handleDic["BUNDA"] = bunda_tag
        pdb.set_trace()
        print(physical_tag)
        print(dirchlet_tag)
        print(neumamn_tag)

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

    def print(self, text = None):
        m1 = self.mb.create_meshset()
        self.mb.add_entities(m1, self.all_nodes)
        m2 = self.mb.create_meshset()
        self.mb.add_entities(m2,self.all_faces)
        m3 = self.mb.create_meshset()
        self.mb.add_entities(m3, self.all_volumes)
        m4 = self.mb.create_meshset()
        self.mb.add_entities(m4, self.all_edges)

        if text == None:
            text = "output"
        extension = ".vtk"
        text1 = text + "-nodes" + extension
        text2 = text + "-face" + extension
        text3 = text + "-volume" + extension
        text4 =  text + "-edges" + extension
        self.mb.write_file(text1,[m1])
        self.mb.write_file(text2,[m2])
        self.mb.write_file(text3,[m3])
        self.mb.write_file(text4,[m4])