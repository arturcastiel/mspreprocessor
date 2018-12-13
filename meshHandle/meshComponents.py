import numpy as np
from pymoab import types, rng
import pdb


class MoabVar(object):
    def __init__(self, core, name_tag, var_type="volumes", data_size=1, data_format="float", data_density="dense"):
        print("classe incializada com sucesso")
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


    def __getitem__(self, index):
        if type(index) == np.ndarray:
            print("ARRAY DO NUMPY")
        print(type(index))
        print(index)

        return 10


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
