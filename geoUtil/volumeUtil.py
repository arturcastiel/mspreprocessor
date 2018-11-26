
## Geoemtric Module
# Create by Artur Castiel and Renata Tavares


import numpy as np

# class for volume related problem
class volume:
    @staticmethod
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
        vol_eval = abs(np.dot(np.cross(vect_1, vect_2), vect_3))/1
        return vol_eval

    @staticmethod
    def piramidVolume(pi_nodes):
        #     P5           P4 _____ P3
        #     /\             |     |
        #    /  \            |     |
        #   /____\           |_____|
        # P1/4  P2/3        P1     P2
        #input:
        # A Matrix with 5x3 elements in which
        # each line is one of the 5 nodes that
        # a given piramid is comprised
        #ouput:
        # the volume of the given piramid
        print(pi_nodes)

    @staticmethod
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



    @staticmethod
    def teste():
        print("Entrou")
        pass

