
## Geoemtric Module
# Create by Artur Castiel and Renata Tavares


import numpy as np

# class for volume related problem
def tetraVolume(tet_nodes):
    #input:
    # A Matrix with 4x3 elements in which
    # each line is one of the 4 nodes that
    # a given tetrahedron is comprised
    #ouput:
    # the volume of the given tetrahedron
    vect_1 = tet_nodes[1] - tet_nodes[0]
    vect_2 = tet_nodes[2] - tet_nodes[0]
    vect_3 = tet_nodes[3] - tet_nodes[0]
    vol_eval = abs(np.dot(np.cross(vect_1, vect_2), vect_3))/6
    return vol_eval

def piramidVolume(pi_nodes):
    #     P5           P4 _____ P3
    #     /\             |     |
    #    /  \            |     |
    #   /____\           |_____|
    # P1/4  P2/3        P1     P2
    #input:
    # A Matrix with 4x3 elements in which
    # each line is one of the 5 nodes that
    # a given piramid is comprised
    # The 3 first nodes lie on the plane of the base (coplanar points) and must be connected.
    # The fourth node of the matrix must be the top point (P5).
    # ouput: the volume of the given piramid
    vect_1 = pi_nodes[1] - pi_nodes[0]
    vect_2 = pi_nodes[2] - pi_nodes[0]
    base_area = abs(np.dot(vect_1, vect_2))

    vect_3 = pi_nodes[3] - pi_nodes[0]
    normal_vect = np.cross(vect_1, vect_2)
    piram_height = np.dot(vect_3, normal_vect)/(np.linalg.norm(normal_vect)

    piram_vol = (1/3)*base_area*piram_height
    return(piram_vol)

def hexahedronVolume(pi_nodes):
    #
    #    ______   <- F2
    #   /     /|
    #  /_____/ |
    #  |     | |
    #  | F1  | /
    #  |_____|/
    #
    #
    # P1 _____P2     P5  ____ P6
    #   |     |         |    |
    #   | F1  |         | F2 |
    #   |_____|         |____|
    # P4      P3     P8       P7
    #
    # F1 - Front Face
    # F2 - Back Face
    #  NOTE:
    #  The given hexahedron may be irregular
    #  The sketch above describes the connectivities
    #
    #input:
    # A Matrix with 8x3 elements in which
    # each line is one of the 8 nodes that
    # a given hexahedron
    #ouput:
    # the volume of the given piramid
    print(pi_nodes)
def teste():
    print("Entrou")
    pass
