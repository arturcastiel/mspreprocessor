import numpy as np
from pymoab import types, rng
import pdb



class MeshEntities(object):
    def __init__(self, core, entity_type):
        self.mb = core.mb
        self.meshset = core.root_set
        if entity_type == "nodes":
            self.elements_handle = core.all_nodes
            self.internal_elements = core.internal_nodes
            self.boundary_elements = core.boundary_nodes
            self.vID = 0
        elif entity_type  == "edges":
            self.elements_handle = core.all_edges
            self.internal_elements = core.internal_edges
            self.boundary_elements = core.boundary_edges
            self.vID = 1
        elif entity_type == "faces":
            self.elements_handle = core.all_faces
            self.internal_elements = core.internal_faces
            self.boundary_elements = core.boundary_faces
            self.vID = 2
        elif entity_type == "volumes":
            self.elements_handle = core.all_volumes
            self.boundary_elements = core.boundary_volumes
            self.vID = 3
        self.tag_handle = core.handleDic["GLOBAL_ID"]
        self.t_range_vec = self.elements_handle
        print(self.tag_handle)
        print("Mesh Entity type {0} successfully intialized".format(entity_type))
        print(self.read(self.boundary_elements))

    def __getitem__(self, index):
        range_vec = self.create_range_vec(index)
        self.t_range_vec = rng.Range(np.asarray(self.elements_handle)[range_vec].astype("uint"))
        return self

    def access_handle(self):
        # input: range of handles of different dimensions

        # returns all entities with d-1 dimension the comprises the given range
        # ie: for a volume, the faces, for a face the edges and for an edge the points.
        #
        handle = self.t_range_vec
        vecdim = self.vID * np.ones(len(self.t_range_vec)).astype(int)
        # pdb.set_trace()
        all_adj = np.array([np.array(self.mb.get_adjacencies(el_handle, dim-1)) for dim, el_handle in zip(vecdim,handle)])
        #unique_adj = np.unique(np.ma.concatenate(all_adj)).astype("uint64")
        pdb.set_trace()
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


    def __call__(self):
        return self.all
    def read(self,handle):
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
    @internal.setter
    def pro(self,data):
        self._data = data



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

    def __setitem__(self,index,data):
        # if isinstance(index, int):
        #     range_vec = np.array([index]).astype("uint")
        # elif isinstance(index, np.ndarray):
        #     if index.dtype == "bool":
        #         range_vec = np.where(index)[0]
        #     else:
        #         range_vec = index
        # elif isinstance(index, slice):
        #     start = index.start
        #     stop = index.stop
        #     step = index.step
        #     #pdb.set_trace()
        #     if start is None:
        #         start = 0
        #     if stop is None:
        #         stop = len(self)
        #     if step is None:
        #         step = 1
        #     range_vec = np.arange(start, stop, step).astype('uint')
        # elif isinstance(index, list):
        #     range_vec = np.array(index)
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
        # if isinstance(index, int):
        #     range_vec = np.array([index])
        #     return self.read_data(range_vec)[0][:]
        # elif isinstance(index, np.ndarray):
        #     range_vec = index
        # elif isinstance(index, slice):
        #     start = index.start
        #     stop = index.stop
        #     step = index.step
        #     if start is None:
        #         start = 0
        #     if stop is None:
        #         stop = len(self)
        #     if step is None:
        #         step = 1
        #     range_vec = np.arange(start, stop, step).astype('uint')
        # elif isinstance(index, list):
        #     range_vec = np.array(index)
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
