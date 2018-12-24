import numpy as np
from pymoab import types, rng
import pdb


class GetItem(object):
    def __init__(self, adj):
        self.fun = adj

    def __call__(self, item):
        return self.fun(item)

    def __getitem__(self, item):
        return self.fun(item)


class MeshEntities(object):
    def __init__(self, core, entity_type):
        self.mb = core.mb
        self.mtu = core.mtu
        self.meshset = core.root_set
        self.nodes = core.all_nodes
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
        if self.vID == 0:
            self.adjacencies = GetItem(self._adjacencies_for_nodes)
            self.coords =  GetItem(self._coords)
        else:
            self.adjacencies = GetItem(self._adjacencies)

        self.classify_element = GetItem(self._classify_element)
        # initialize specific flag dic in accordance with type of the object create
        self.flag = {key: self.read(value[self.vID]) for key, value in core.flag_dic.items()
                     if value[self.vID].empty() is not True}

        print("Mesh Entity type {0} successfully initialized".format(entity_type))


    def bridge_adjacencies(self, index, interface, target):
        # lacks support for indexing with multiple numbers
        range_vec = self.create_range_vec(index)
        all_bridge = [self.mtu.get_bridge_adjacencies(el_handle, self.num[interface], self.num[target]) for el_handle
                      in self.range_index(range_vec)]
        inside_meshset = self.mb.get_entities_by_handle(self.meshset)
        all_brige_in_meshset = [rng.intersect(el_handle, inside_meshset) for el_handle in all_bridge]
        all_briges_in_meshset_id = np.array([self.read(el_handle) for el_handle in all_brige_in_meshset])
        return all_briges_in_meshset_id

    def _coords(self, index):
        range_vec = self.create_range_vec(index)
        element_handle = self.range_index(range_vec, True)
        return np.reshape(self.mb.get_coords(element_handle),(-1,3))

    def _adjacencies_for_nodes(self, index):
        return self.create_range_vec(index)

    def _adjacencies(self, index,flag_nodes=False):
        range_vec = self.create_range_vec(index)
        if not flag_nodes:
            dim_tag = self.vID - 1
        else:
            dim_tag = 0
        all_adj = [self.mb.get_adjacencies(el_handle, dim_tag) for el_handle in self.range_index(range_vec)]
        adj_id = np.array([self.read(el_handle) for el_handle in all_adj])
        return adj_id

    def create_range_vec(self, index):
        range_vec = None
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

    def _classify_element(self, index):
        range_vec = self.create_range_vec(index)
        range = self.range_index(range_vec)
        type_list = np.array([self.mb.type_from_handle(el) for el in range])
        return  type_list

    def range_index(self, vec_index, flag_nodes=False):
        if not flag_nodes:
            range_handle = self.elements_handle
        else:
            range_handle = self.nodes
        if vec_index.dtype == "bool":
            vec = np.where(vec_index)[0]
        else:
            vec = vec_index.astype("uint")
        handles = np.asarray(range_handle)[vec.astype("uint")].astype("uint")
        return rng.Range(handles)

    def __str__(self):
        string = "{0} object \n Total of {1} {0} \n {2}  boundary {0} \n {3} internal {0}".format(self.entity_type,
            len(self.elements_handle), len(self.boundary_elements), len(self.internal_elements))
        return string

    def __len__(self):
        return len(self.elements_handle)

    def __call__(self):
        return self.all

    def read(self, handle):
        return self.mb.tag_get_data(self.tag_handle, handle).ravel()

    @property
    def all_flagged_elements(self):
        return np.array(  list(self.flag.values())).astype(int)

    @property
    def all_flags(self):
        return np.array(list(self.flag.keys())).astype(int)

    @property
    def all(self):
        return self.read(self.elements_handle)

    @property
    def boundary(self):
        return self.read(self.boundary_elements)

    @property
    def internal(self):
        return self.read(self.internal_elements)


class MoabVariable(object):
    def __init__(self, core, name_tag, var_type="volumes", data_size=1, data_format="float", data_density="sparse",
                 entity_index=None):
        # pdb.set_trace()
        self.mb = core.mb
        self.var_type = var_type
        self.data_format = data_format
        self.data_size = data_size
        self.data_density = data_density
        self.name_tag = name_tag
        self.custom = False

        if var_type == "nodes":
            self.elements_handle = core.all_nodes
        elif var_type == "edges":
            self.elements_handle = core.all_edges
        elif var_type == "faces":
            self.elements_handle = core.all_faces
        elif var_type == "volumes":
            self.elements_handle = core.all_volumes

        if entity_index is not None:
            self.elements_handle = self.range_index(entity_index)
            self.custom = True

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
        if isinstance(data, int) or isinstance(data, float) or isinstance(data, bool):
            data = data * np.ones((range_vec.shape[0], self.data_size)).astype(self.data_format)
        elif (isinstance(data, np.ndarray)) and (len(data) == self.data_size):
            data = data * np.tile(data, (range_vec.shape[0], 1)).astype(self.data_format)
        elif isinstance(data, list) & (len(data) == self.data_size):
            data = np.array(data)
            data = data * np.tile(data, (range_vec.shape[0], 1)).astype(self.data_format)
        self.set_data(data, index_vec=range_vec)

    def __getitem__(self, index):
        range_vec = self.create_range_vec(index)
        if isinstance(index, int):
            return self.read_data(range_vec)[0][:]
        else:
            return self.read_data(range_vec)

    def __str__(self):
        string = "{0} variable: {1} based - Type: {2} - Length: {3} - Data Type: {4}"\
            .format(self.name_tag.capitalize(), self.var_type.capitalize(), self.data_format.capitalize(),
                    self.data_size, self.data_density.capitalize())
        if self.custom:
            string = string + " - Custom variable"
        return string

    def __len__(self):
        return len(self.elements_handle)

    def create_range_vec(self, index):
        range_vec = None
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
        if index_vec.size > 0:
            range_el = self.range_index(index_vec)
        else:
            range_el = self.elements_handle
        self.mb.tag_set_data(self.tag_handle, range_el, data)

    def read_data(self, index_vec=np.array([])):
        if index_vec.size > 0:
            range_el = self.range_index(index_vec)
        else:
            range_el = self.elements_handle
        return self.mb.tag_get_data(self.tag_handle, range_el)