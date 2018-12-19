
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
    # The 3 first nodes lie on the plane of the base (coplanar points) and must be connected. The fourth node of the matrix must be the top point (P5).
    # ouput: the volume of the given piramid
    vect_1 = pi_nodes[1] - pi_nodes[0]
    vect_2 = pi_nodes[2] - pi_nodes[0]
    base_area = abs(np.dot(vect_1, vect_2))

    vect_3 = pi_nodes[3] - pi_nodes[0]
    normal_vect = np.cross(vect_1, vect_2)
    piram_height = np.dot(vect_3, normal_vect)/(np.linalg.norm(normal_vect)

    piram_vol = (1/3)*base_area*piram_height
    return(piram_vol)

def hexahedronVolume(hexa_nodes):
    #
    #    ______   <- F2
    #   /     /|
    #  /_____/ |
    #  |     | |
    #  | F1  | /
    #  |_____|/
    #
    #
    # P4 _____P5     P6  ____ P7
    #   |     |         |    |
    #   | F1  |         | F2 |
    #   |_____|         |____|
    # P0      P1     P2       P3
    #
    # F1 - Front Face
    # F2 - Back Face
    #  NOTE:
    # The given hexahedron may be irregular
    # The method used here includes this possibility
    # The sketch above describes the connectivities
    #
    # Input:
    # A Matrix with 8x3 elements in which
    # each line is one of the 8 nodes that
    # a given hexahedron. The sequence of
    # the nodes in the matrix must be the
    # same as the figure.
    #
    # Ouput:
    # The volume of the given hexahedron

    vetor = np.cross((hexa_nodes[7]-hexa_nodes[0]), (hexa_nodes[1]-hexa_nodes[0]))
    volume1 = np.dot(vetor, (hexa_nodes[3]-hexa_nodes[5]))

    vetor2 = np.cross((hexa_nodes[7]-hexa_nodes[0]), (hexa_nodes[4]-hexa_nodes[0]))
    volume2 = np.dot(vetor2,(hexa_nodes[5]-hexa_nodes[6]))

    vetor3 = np.cross((hexa_nodes[7]-hexa_nodes[0]), (hexa_nodes[2]-hexa_nodes[0]))
    volume3 = np.dot(vetor3, (hexa_nodes[6]-hexa_nodes[3]))

    hexa_vol = (volume1+volume2+volume3)/6
    return (hexa_vol)

def teste():
    print("Entrou")
    pass
