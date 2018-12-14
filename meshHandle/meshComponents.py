import numpy as np
from pymoab import types, rng
import pdb


class MoabVar(object):
    def __init__(self, core, name_tag, var_type="volumes", data_size=1, data_format="float", data_density="sparse"):
        print("Component Class Successfully intialized")
        # pdb.set_trace()
        self.mb = core.mb
        self.var_type = var_type
        self.data_format = data_format
        self.data_size = data_size
        self.data_density = data_density
        self.name_tag = name_tag

        if var_type == "nodes":
            self.elements_handle = core.all_nodes
        elif var_type == "edges":
            self.elements_handle = core.all_edges
        elif var_type == "faces":
            self.elements_handle = core.all_faces
        elif var_type == "volumes":
            self.elements_handle = core.all_volumes
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

    def __call__(self):
        return self.mb.tag_get_data(self.tag_handle, self.elements_handle)

    def __setitem__(self,index,data):
        if isinstance(index, int):
            range_vec = np.array([index])
        elif isinstance(index, np.ndarray):
            range_vec = index
        elif isinstance(index, slice):
            start = index.start
            stop = index.stop
            step = index.step
            #pdb.set_trace()
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if step is None:
                step = 1
            range_vec = np.arange(start, stop, step).astype('uint')
        elif isinstance(index, list):
            range_vec = np.array(index)

        self.set_data(data, index_vec = range_vec)
        # if isinstance(data, int):
        #     data = data* np.ones((len(self),self.data_size)).astype(self.data_format)

        print(data)
        pass

    def __getitem__(self, index):
        if isinstance(index, int):
            range_vec = np.array([index])
            return self.read_data(range_vec)[0][:]
        elif isinstance(index, np.ndarray):
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
            range_vec = np.arange(start, stop, step).astype('uint')
        elif isinstance(index, list):
            range_vec = np.array(index)
        return self.read_data(range_vec)


    def __str__(self):
        string = "{0} variable: {1} based - {2} type - {3} length - data {4}".format(self.name_tag, self.var_type,
                                                                                     self.data_format, self.data_size,
                                                                                     self.data_density)
        return string

    def __len__(self):
        return len(self.elements_handle)

    def range_index(self, vec_index):
        range_handle = self.elements_handle
        if vec_index.dtype == "bool":
            vec = np.where(vec_index)[0]
        else:
            vec = vec_index.astype("uint")
        handles = np.asarray(range_handle)[vec.astype("uint")].astype("uint")
        return rng.Range(handles)

    def set_data(self, data, index_vec=np.array([])):
        pdb.set_trace()
        if index_vec.size > 0:
            range_el = self.range_index(index_vec)
        else:
            range_el = self.elements_handle
        if len(data) != len(range_el):
            print("Operation failed: Range handle and data vector mismatch")
        self.mb.tag_set_data(self.tag_handle, range_el, data)

    def read_data(self, index_vec=np.array([])):
        if index_vec.size > 0:
            range_el = self.range_index(index_vec)
        else:
            range_el = self.elements_handle
        return self.mb.tag_get_data(self.tag_handle, range_el)
