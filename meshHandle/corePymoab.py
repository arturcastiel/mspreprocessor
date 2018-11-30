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
        self.check_integrity()
        self.handleDic = {}
        self.flag_dic = {}
        self.read_flags()
        self.read_parallel()
        self.create_parallel_meshset()
        #self.create_flag_tag()
        #pdb.set_trace()
        #print(self.access_handle(self.all_nodes[0]))
        #pdb.set_trace()
        #self.create_flag_tag()

    def check_integrity(self):
        # check if the mesh contains
        check_list = [len(self.all_nodes), len(self.all_edges), len(self.all_faces), len(self.all_volumes)]
        list_words = ['Nodes', "Edges", "Faces", "Volumes"]
        print("Checking mesh integrity:")
        index = 0
        for entity in check_list:
            if entity > 0:
                print(list_words[index] + " successfully imported")
            else:
                print("------------------------------\nError creating \n" +
                      list_words[index] + " was not imported")
            index += 1

    def create_parallel_meshset(self):
        try:
            parallel_tag = self.mb.tag_get_handle("PARALLEL_PARTITION")
            flag = False
        except:
            print("Parallel Partition Tag not found \nAborting creating parallel partition entities.")
            flag = True
        if not flag:
            print("Parallel Partition Tag detected \nCreating parallel partitions entities")
            self.handleDic["PARALLEL_PARTITION"] = parallel_tag
            parallel_sets = self.mb.get_entities_by_type_and_tag(
                0, types.MBENTITYSET, np.array(
                (parallel_tag,)), np.array((None,)))
            self.deftagHandle("PARALLEL",dataSize=1,dataText="int")
            partition_volumes = []
            for set in parallel_sets:
                num_tag = self.readData("PARALLEL_PARTITION", rangeEl = set)[0,0]
                list_entity = [self.mb.get_entities_by_dimension(set, 0), self.mb.get_entities_by_dimension(set, 1),
                               self.mb.get_entities_by_dimension(set, 2), self.mb.get_entities_by_dimension(set, 3)]
                # print([num_tag, entities])
                partition_volumes.append(list_entity)
        return partition_volumes



    def read_parallel(self):
        try:
            parallel_tag = self.mb.tag_get_handle("PARALLEL_PARTITION")
            flag = False
        except:
            print("Parallel Partition Tag not found \nMesh initialized with no parallel partition")
            flag = True
        if not flag:
            print("Parallel Partition Tag detected \nMesh initialized with a parallel partition")
            self.handleDic["PARALLEL_PARTITION"] = parallel_tag
            parallel_sets = self.mb.get_entities_by_type_and_tag(
                0, types.MBENTITYSET, np.array(
                (parallel_tag,)), np.array((None,)))
            self.deftagHandle("PARALLEL",dataSize=1,dataText="int")
            for set in parallel_sets:
                num_tag = self.readData("PARALLEL_PARTITION", rangeEl = set)
                entities = self.mb.get_entities_by_dimension(set, 3)
                # print([num_tag, entities])
                vec = np.ones(len(entities)).astype(int) * num_tag[0,0]
                self.setData("PARALLEL",data = vec,rangeEl=entities)

    def read_flags(self):
        physical_tag = self.mb.tag_get_handle("MATERIAL_SET")
        physical_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (physical_tag,)), np.array((None,)))
        self.handleDic["MATERIAL_SET"] = physical_tag
        flag_list = np.array([])
        for set in physical_sets:
            bc_flag = self.readData("MATERIAL_SET", rangeEl=set)[0,0]
            flag_list = np.append(flag_list,bc_flag)
            list_entity = [self.mb.get_entities_by_dimension(set,0), self.mb.get_entities_by_dimension(set,1),
                         self.mb.get_entities_by_dimension(set,2), self.mb.get_entities_by_dimension(set,3)]
            self.flag_dic[bc_flag] = list_entity
        self.flag_list = flag_list.sort(axis=0)
        # self.handleDic["MATERIAL_SET"] = physical_tag
        # self.deftagHandle("FLAGS", 1, dataText="int",dataDensity="sparse")
        # self.deftagHandle("MATERIAL", 1, dataText="int",dataDensity="sparse")
        # self.init_tag("MATERIAL")
        # self.init_tag("FLAGS")

    def access_meshset(self, handle):
        # returns the entities contained inside a give meshset handle
        # ie: for a meshset handle the entities inside are returned
        temp_range = []
        for el in range(self.dimension+1):
            subel = (self.mb.get_entities_by_dimension(handle, el))
            temp_range.append(subel)
        temp_range.append(self.mb.get_entities_by_dimension(handle, 11))
        return temp_range

    def access_handle(self,handle):
        # returns the entities contained inside a give handle
        # ie: for a volume, the faces, for a face the edges and
        #     for an edge the points.
        # to be improved - > check issues with the range class
        flag = 0
        tmp = []
        for el in range(3):
            tmp.append(self.mb.get_adjacencies(handle, el))
        return tmp

    def create_flag_tag(self):
        print("Creating Flag Tag")
        physical_tag = self.mb.tag_get_handle("MATERIAL_SET")
        physical_sets = self.mb.get_entities_by_type_and_tag(
            0, types.MBENTITYSET, np.array(
            (physical_tag,)), np.array((None,)))
        self.handleDic["MATERIAL_SET"] = physical_tag
        self.deftagHandle("FLAGS", 1, dataText="int")
        self.deftagHandle("MATERIAL", 1, dataText="int")
        #self.init_tag("MATERIAL")
        self.init_tag("FLAGS")
        for bcset in physical_sets:
            bc_flags = self.readData("MATERIAL_SET", rangeEl=bcset)
            entity_list = self.range_merge(self.mb.get_entities_by_dimension(bcset, 0),
                                           self.mb.get_entities_by_dimension(bcset, 1),
                                           self.mb.get_entities_by_dimension(bcset, 2),
                                           self.mb.get_entities_by_dimension(bcset, 3))
            print([entity_list, bc_flags[0,0]])
            vec = np.ones(len(entity_list)).astype(int) * (bc_flags[0, 0])
            if bc_flags[0, 0] < 100:
                print("MATERIAL FLAG DE MATERIAL GRAVADO")
                self.setData("MATERIAL", data=vec, rangeEl=entity_list)
            elif bc_flags[0, 0] > 100:
                print("FLAG FLAG DE FLAGL GRAVADO")
                self.setData("FLAGS", data=vec, rangeEl=entity_list)

    def deftagHandle(self,nameTag,dataSize, dataText = "float", dataDensity = "dense"):
         if dataDensity == "dense":
             dataDensity = types.MB_TAG_DENSE
         elif dataDensity == "sparse":
             dataDensity = types.MB_TAG_SPARSE
         elif dataDensity == "bit":
             dataDensity = types.MB_TAG_BIT
         else:
             print("Please define a valid tag type")
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

    def init_tag(self,nametag,dtype = "int", entityType = 4 ):
        # initialize a tag
        # zeros nodes, edges, faces and volumes
        # by default it zeros all geometric entities
        if dtype == "int":
            var_type = int
        elif dtype == "float":
            var_type = float
        elif dtype == "bool":
            var_type = bool
        el = [[self.all_nodes], [self.all_edges], [self.all_faces], [self.all_volumes],
              [self.all_nodes, self.all_edges, self.all_faces, self.all_volumes]]
        range_temp = self.range_merge(*el[entityType])
        self.setData(nametag,data = np.zeros(len(range_temp)).astype(var_type),rangeEl = range_temp)

    @staticmethod
    def range_merge(*args):
        range_merged = rng.Range()
        for arg in args:
                range_merged.merge(arg)
        return range_merged

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
        text4 = text + "-edges" + extension
        text5 = text + "-all" + extension
        self.mb.write_file(text1,[m1])
        self.mb.write_file(text2,[m2])
        self.mb.write_file(text3,[m3])
        self.mb.write_file(text4,[m4])
        self.mb.write_file(text5)