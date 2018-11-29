# Procedure to get the relevant vertices for the geometric module in each type of elements

from pymoab import core, topo_util, rng


mb = core.Core()
mesh_topo_util = topo_util.MeshTopoUtil(mb)
# Piramide

def get_piramid_adjacencies(pi_nodes):
    vertices = create_vertices(pi_nodes)
    element = create_element(types.MBPYRAMID, vertices)
    edges = mbcore.get_adjacencies(element, 1, True)
    adjacencies = mesh_topo_util.get_bridge_adjacencies(vertices, 1, 0)

base_nodes = rng.Range()
top_node = rng.Range()
i = 0

for i in range(0,len(adjacencies)):
    if len(adjacencies[i]) == 3:
        base_nodes.insert(vertices[i])
    else:
        top_node.insert(vertices[i])

aux = mesh_topo_util.get_bridge_adjacencies(base_nodes[0], 1, 0)
coords1 = get_coords(base_nodes[0])
coords2 = get_coords(aux[0])
coords3 = get_coords(aux[1])
coords4 = get_coords(top_node)
order = np.array([coords1], [coords2], [coords3], [coords4])

return parameter
