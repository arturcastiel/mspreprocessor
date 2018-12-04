from pymoab import core, types, rng, topo_util
from pymoab import skinner as sk
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

        self.skinner_test()



        self.init_id()
        self.check_integrity()
        self.create_id_visualization()
        self.flag_dic = {}
        self.read_flags()

        self.create_flag_visualization()
        self.create_flag_visualization()

        # swtich on/off
        self.parallel_meshset = self.create_parallel_meshset()
        self.create_parallel_visualization()


    def __show_edges_matrix(self):
        tmp_matrix = np.zeros((len(self.all_edges),2))
        for el,index in zip(self.all_edges, range(len(self.all_edges))):
            tmp_matrix[index] = self.mb.get_adjacencies(el,0)
        return tmp_matrix

    def init_id(self):
        # delete previous IDs
        # Gmesh standard counts from 1
        # GLOBAL_ID_tag = self.mb.tag_get_handle(
        #    "Global_ID", 1, types.MB_TYPE_INTEGER, types.MB_TAG_DENSE, False)

        GLOBAL_ID_tag = self.mb.tag_get_handle(
            "GLOBAL_ID", 1, types.MB_TYPE_INTEGER, types.MB_TAG_DENSE, False)

        self.handleDic["GLOBAL_ID"] = GLOBAL_ID_tag
        # create volume ids
        self.setData("GLOBAL_ID", np.arange(len(self.all_volumes)))
        # create face ids
        self.setData("GLOBAL_ID", np.arange(len(self.all_faces)),rangeEl = self.all_faces)
        # create edges ids
        self.setData("GLOBAL_ID", np.arange(len(self.all_edges)),rangeEl = self.all_edges)
        # create nodes ids
        self.setData("GLOBAL_ID", np.arange(len(self.all_nodes)),rangeEl = self.all_nodes)

    def skinner_test(self):
        skin = sk.Skinner(self.mb)
        print("Entering skinner test")

        # geo_tag = self.mb.tag_get_handle("GEOM_DIMENSION")
        # self.handleDic["GEOM_DIMENSION"] = geo_tag
        # self.setData("GEOM_DIMENSION", np.arange(len(self.all_volumes)))
        # # # create face ids
        # self.setData("GEOM_DIMENSION", np.arange(len(self.all_faces)),rangeEl = self.all_faces)
        # # # create edges ids
        # self.setData("GEOM_DIMENSION", np.arange(len(self.all_edges)),rangeEl = self.all_edges)
        # # create nodes ids
        # self.setData("GEOM_DIMENSION", np.arange(len(self.all_nodes)),rangeEl = self.all_nodes)

        flag = False
        #ol = teste.find_geometric_skin( self.mb.get_root_set())

        #vertex_on_skin_handles2 = skin.find_geometric_skin(self.mb.get_root_set(),exceptions =((16)))

        vertex_on_skin_handles = skin.find_skin( self.mb.get_root_set(), self.all_volumes[:]) #, True,False)
        print(vertex_on_skin_handles)

        # vertex_ids = self.readData("GLOBAL_ID", rangeEl = vertex_on_skin_handles)
        pdb.set_trace()

        self.deftagHandle("SKINPOINT",1, "int", dataDensity="sparse")
        self.setData("SKINPOINT", 200*np.ones(len(vertex_on_skin_handles)).astype(int), rangeEl = vertex_on_skin_handles)


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

    def create_parallel_visualization(self):
        k = 0
        for sets in self.parallel_meshset:
            for dim in sets:
                if len(dim) != 0:
                    self.setData("PARALLEL", k * np.ones(len(dim)).astype(int), rangeEl=dim)
            k += 1

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

    def create_flag_visualization(self):
        self.deftagHandle("FLAGS", 1, dataText="int")
        self.deftagHandle("MATERIAL", 1, dataText="int")
        for k in self.flag_dic:
            sets = self.flag_dic[k]
            for dim in sets:
                if len(dim) != 0:
                    if k > 100:
                        self.setData("FLAGS", k * np.ones(len(dim)).astype(int), rangeEl=dim)
                    else:
                        self.setData("MATERIAL", k * np.ones(len(dim)).astype(int), rangeEl=dim)

    def create_flag_visualization_alternative(self):
        self.deftagHandle("FLAGS-NODES", 1, dataText="int")
        self.deftagHandle("FLAGS-EDGES", 1, dataText="int")
        self.deftagHandle("FLAGS-FACES", 1, dataText="int")
        self.deftagHandle("FLAGS-VOUMES", 1, dataText="int")
        for k in self.flag_dic:
            sets = self.flag_dic[k]
            for dim, ndim in zip(sets,range(4)):

                if len(dim) != 0:
                    print([k, ndim])
                    if k > 100:
                        if ndim == 0:
                            # print([dim, k])
                            self.setData("FLAGS-NODES", k * np.ones(len(dim)).astype(int), rangeEl=dim)
                        elif ndim == 1:
                            # print([dim, k])
                            self.setData("FLAGS-EDGES", k * np.ones(len(dim)).astype(int), rangeEl=dim)
                        elif ndim ==2:
                            # print([dim, k])
                            self.setData("FLAGS-FACES", k * np.ones(len(dim)).astype(int), rangeEl=dim)
                        elif ndim == 3:
                            # print([dim, k])
                            self.setData("FLAGS-VOLUMES", k * np.ones(len(dim)).astype(int), rangeEl=dim)
                    else:
                        # self.setData("MATERIAL", k * np.ones(len(dim)).astype(int), rangeEl=dim)
                        pass

    def create_id_visualization(self):
        self.deftagHandle("ID-NODES", 1, dataText="int")
        self.deftagHandle("ID-EDGES", 1, dataText="int")
        self.deftagHandle("ID-FACES", 1, dataText="int")
        self.deftagHandle("ID-VOLUMES", 1, dataText="int")

        data_node = self.readData("GLOBAL_ID", rangeEl=self.all_nodes)
        data_edges = self.readData("GLOBAL_ID", rangeEl=self.all_edges)
        data_faces= self.readData("GLOBAL_ID", rangeEl=self.all_faces)
        data_volumes = self.readData("GLOBAL_ID", rangeEl=self.all_volumes)

        self.setData("ID-NODES", data_node, rangeEl=self.all_nodes)
        self.setData("ID-EDGES", data_edges, rangeEl=self.all_edges)
        self.setData("ID-FACES", data_faces, rangeEl=self.all_faces)
        self.setData("ID-VOLUMES", data_volumes, rangeEl=self.all_volumes)


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

    def check_handle_dimension(self,handle,*args):
        # INPUT: handle or range
        # OUTPUT: handles in the range of the dimension in args
        # 0 - nodes , 1 -edges, 2 - faces 3 - volumes, 4- meshset
        handle_int = np.asarray(handle).astype("uint64")
        type_list =np.array([self.mb.type_from_handle(el) for el in  handle_int])
        handle_classification = np.zeros(len(handle))
        nodetype = type_list == types.MBVERTEX
        edgetype = type_list == types.MBEDGE
        facetype = (type_list == types.MBTRI) | (type_list == types.MBQUAD) | (type_list == types.MBPOLYGON)
        volumetype =  (type_list == types.MBTET) | (type_list == types.MBPYRAMID) | (type_list == types.MBPRISM) | \
                      (type_list == types.MBKNIFE) | (type_list == types.MBHEX) | (type_list == types.MBPOLYHEDRON)
        meshsettype =  type_list ==  types.MBENTITYSET
        handle_classification[nodetype] = 0
        handle_classification[edgetype] = 1
        handle_classification[facetype] = 2
        handle_classification[volumetype] = 3
        handle_classification[meshsettype] = 4
        test_elem = np.array([*args])
        return rng.Range(handle_int[np.isin(handle_classification,test_elem)])


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
        text6 = text + "-together" + extension
        self.mb.write_file(text1,[m1])
        self.mb.write_file(text2,[m2])
        self.mb.write_file(text3,[m3])
        self.mb.write_file(text4,[m4])
        self.mb.write_file(text5)
