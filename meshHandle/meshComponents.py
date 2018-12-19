import numpy as np
from pymoab import types, rng
import pdb


class GetItem(object):
    def __init__(self, adj):
        self.fun = adj

    def __call__(self, item):
        return self.funj(item)

    def __getitem__(self, item):
        return self.fun(item)


class MeshEntities(object):
    def __init__(self, core, entity_type):
        self.mb = core.mb
        self.mtu = core.mtu
        self.meshset = core.root_set
        self.num = {"nodes": 0, "node": 0, "edges": 1, "edge": 1, "faces": 2, "face": 2, "volumes": 3, "volume": 3,
                    0: 0, 1: 1, 2: 2, 3: 3}

        string = {0: "nodes", 1: "edges", 2: "faces", 3: "volumes"}
        entity_num = self.num[entity_type]
        if entity_num == 0:
            self.elements_handle = core.all_nodes
            self.internal_elements = core.internal_nodes
            self.boundary_elements = core.boundary_nodes
            self.vID = 0
        elif entity_num == 1:
            self.elements_handle = core.all_edges
            self.internal_elements = core.internal_edges
            self.boundary_elements = core.boundary_edges
            self.vID = 1
        elif entity_num == 2:
            self.elements_handle = core.all_faces
            self.internal_elements = core.internal_faces
            self.boundary_elements = core.boundary_faces
            self.vID = 2
        elif entity_num == 3:
            self.elements_handle = core.all_volumes
            self.internal_elements = core.internal_volumes
            self.boundary_elements = core.boundary_volumes
            self.vID = 3
        self.entity_type = string[entity_num]
        self.tag_handle = core.handleDic["GLOBAL_ID"]
        self.t_range_vec = self.elements_handle
        self.adjacencies = GetItem(self._adjacencies)

        print("Mesh Entity type {0} successfully intialized".format(entity_type))

    def adjacencies_bridge(self, index, interface, target):
        # lacks support for indexing with multiple numbers
        range_vec = self.create_range_vec(index)
        all_bridge = [self.mtu.get_bridge_adjacencies(el_handle, self.num[interface], self.num[target]) for el_handle
                      in self.range_index(range_vec)]
        inside_meshset = self.mb.get_entities_by_handle(self.meshset)
        all_brige_in_meshset = [rng.intersect(el_handle, inside_meshset) for el_handle in all_bridge]
        all_briges_in_meshset_id = np.array([self.read(el_handle) for el_handle in all_brige_in_meshset])
        return all_briges_in_meshset_id

    def _adjacencies(self, index):
        range_vec = self.create_range_vec(index)
        dim_tag = self.vID -1
        all_adj = [self.mb.get_adjacencies(el_handle, dim_tag) for el_handle in self.range_index(range_vec)]
        adj_id = np.array([self.read(el_handle) for el_handle in all_adj])
        return adj_id

    def access_handle(self):
        # input: range of handles of different dimensions

        # returns all entities with d-1 dimension the comprises the given range
        # ie: for a volume, the faces, for a face the edges and for an edge the points.
        #
        handle = self.t_range_vec
        vecdim = self.vID * np.ones(len(self.t_range_vec)).astype(int)
        all_adj = np.array([np.array(self.mb.get_adjacencies(el_handle, dim-1)) for dim, el_handle in zip(vecdim,handle)])
        unique_adj = np.unique(np.concatenate(all_adj)).astype("uint64")
        return rng.Range(unique_adj)

    def create_range_vec(self, index):
        if isinstance(index, int):
            range_vec = np.array([index]).astype("uint")
        elif isinstance(index, np.ndarray):
            if index.dtype == "bool":
                range_vec = np.where(index)[0]
            else:
                range_vec = index
        elif isinstance(index, slice):
            start = index.start
            stop = index.stop
            step = index.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if step is None:
                step = 1
            if start < 0:
                start = len(self) + start + 1
            if stop < 0:
                stop = len(self) + stop + 1
            range_vec = np.arange(start, stop, step).astype('uint')
        elif isinstance(index, list):
            range_vec = np.array(index)
        return range_vec

    def range_index(self, vec_index):
        range_handle = self.elements_handle
        if vec_index.dtype == "bool":
            vec = np.where(vec_index)[0]
        else:
            vec = vec_index.astype("uint")
        handles = np.asarray(range_handle)[vec.astype("uint")].astype("uint")
        return rng.Range(handles)

    def __str__(self):
        string = "{0} variable: {1} based - {2} type - {3} length - data {4}".format(self.name_tag, self.var_type,
                                                                                     self.data_format, self.data_size,
                                                                                     self.data_density)
        return string

    def __len__(self):
        return len(self.elements_handle)

    def __call__(self):
        return self.all

    def read(self, handle):
        return self.mb.tag_get_data(self.tag_handle, handle).ravel()

    @property
    def all(self):
        return self.read(self.elements_handle)

    @property
    def boundary(self):
        return self.read(self.boundary_elements)

    @property
    def internal(self):
        return self.read(self.internal_elements)
    #
    # @internal.setter
    # def pro(self,data):
    #     self._data = data






class MoabVariable(object):
    def __init__(self, core, name_tag, var_type="volumes", data_size=1, data_format="float", data_density="sparse", entity_handle = None):
        # pdb.set_trace()
        self.mb = core.mb
        self.var_type = var_type
        self.data_format = data_format
        self.data_size = data_size
        self.data_density = data_density
        self.name_tag = name_tag
        if entity_handle == None:
            if var_type == "nodes":
                self.elements_handle = core.all_nodes
            elif var_type == "edges":
                self.elements_handle = core.all_edges
            elif var_type == "faces":
                self.elements_handle = core.all_faces
            elif var_type == "volumes":
                self.elements_handle = core.all_volumes
        else:
            self.elements_handle = entity_handle
        if data_density == "dense":
            data_density = types.MB_TAG_DENSE
        elif data_density == "sparse":
            data_density = types.MB_TAG_SPARSE
        elif data_density == "bit":
            data_density = types.MB_TAG_BIT
        else:
            print("Please define a valid tag type")
        if data_format == 'float':
            data_format = types.MB_TYPE_DOUBLE
        elif data_format == "int":
            data_format = types.MB_TYPE_INTEGER
        elif data_format == "bool":
            data_format = types.MB_TYPE_BIT
        self.tag_handle = self.mb.tag_get_handle(name_tag, data_size, data_format, data_density, True)
        print("Component class {0} successfully intialized".format(self.name_tag))

    def __call__(self):
        return self.mb.tag_get_data(self.tag_handle, self.elements_handle)

    def __setitem__(self, index, data):
        range_vec = self.create_range_vec(index)
        if isinstance(data, int) or isinstance(data, float) or isinstance(data, bool) :
            data = data * np.ones((range_vec.shape[0],self.data_size)).astype(self.data_format)
        elif (isinstance(data, np.ndarray)) and (len(data) == self.data_size) :
            data = data * np.tile(data,(range_vec.shape[0],1)).astype(self.data_format)
        elif isinstance(data, list) & (len(data) == self.data_size):
            data = np.array(data)
            data = data * np.tile(data,(range_vec.shape[0],1)).astype(self.data_format)
        self.set_data(data, index_vec = range_vec)

    def __getitem__(self, index):
        range_vec = self.create_range_vec(index)
        if isinstance(index, int):
            return self.read_data(range_vec)[0][:]
        else:
            return self.read_data(range_vec)

    def __str__(self):
        string = "{0} variable: {1} based - {2} type - {3} length - data {4}".format(self.name_tag, self.var_type,
                                                                                     self.data_format, self.data_size,
                                                                                     self.data_density)
        return string

    def __len__(self):
        return len(self.elements_handle)


    def create_range_vec(self, index):
        if isinstance(index, int):
            range_vec = np.array([index]).astype("uint")
        elif isinstance(index, np.ndarray):
            if index.dtype == "bool":
                range_vec = np.where(index)[0]
            else:
                range_vec = index
        elif isinstance(index, slice):
            start = index.start
            stop = index.stop
            step = index.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if step is None:
                step = 1
            if start < 0:
                start = len(self) + start + 1
            if stop < 0:
                stop = len(self) + stop + 1
            range_vec = np.arange(start, stop, step).astype('uint')
        elif isinstance(index, list):
            range_vec = np.array(index)
        return range_vec


    def range_index(self, vec_index):
        range_handle = self.elements_handle
        if vec_index.dtype == "bool":
            vec = np.where(vec_index)[0]
        else:
            vec = vec_index.astype("uint")
        handles = np.asarray(range_handle)[vec.astype("uint")].astype("uint")
        return rng.Range(handles)

    def set_data(self, data, index_vec=np.array([])):
        #pdb.set_trace()
        if index_vec.size > 0:
            range_el = self.range_index(index_vec)
        else:
            range_el = self.elements_handle
        # if len(data) != len(range_el):
        #     print("Operation failed: Range handle and data vector mismatch")
        self.mb.tag_set_data(self.tag_handle, range_el, data)

    def read_data(self, index_vec=np.array([])):
        if index_vec.size > 0:
            range_el = self.range_index(index_vec)
        else:
            range_el = self.elements_handle
        return self.mb.tag_get_data(self.tag_handle, range_el)
