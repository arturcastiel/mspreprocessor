
## Geoemtric Module
# Create by Artur Castiel and Renata Tavares
import numpy as np

class geometric_functionalities:
    def tetraVolume(self, tet_nodes):
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

    def hexahedron_volume(self, hexa_nodes):
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
        return hexa_vol

   def piramid_volume(self, pi_nodes): # NÃO ATENDE A TODOS TIPOS DE PIRÂMIDE
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

        piramid_volume = (1/3)*base_area*piram_height
        return piramid_volume

    def triangle_area(self, face_nodes):
        #
        #     P1
        #     |\
        #    |  \
        #   |____\
        # P0      P2
        vector[0] = face_nodes[0]-face_nodes[1]
        vector[1] = face_nodes[0]-face_nodes[2]
        vector[2] = face_nodes[1]-face_nodes[2]
        for i in range (3):
            norm[i] = np.linalg.norm(vector[i])
        semi_perimeter = (norm[0]+norm[1]+norm[2])/2
        triangle_area = np.sqrt(semi_perimeter*(semi_perimeter-norm[0])*(semi_perimeter-norm[1])*(semi_perimeter-norm[2]))
        return triangle_area

    def quadrilateral_area(self, face_nodes):
        #
        # P1 _____P2
        #   |    |
        #   |    |
        #   |____|
        # P0      P3
        #

        #  NOTE:
        # The given quadrilateral may be irregular
        # The method used here includes this possibility
        # The sketch above describes the connectivities
        # Heron's formula is being used here. The
        # quadrilateral was splitted in two triangles
        #
        # Input:
        # A Matrix with 4x3 elements in which
        # each line is one of the 4 nodes that
        # a given hexahedron. The sequence of
        # the nodes in the matrix must be the
        # same as the figure.
        #
        # Ouput:
        # The volume of the given hexahedron

        vector[0] = face_nodes[0]-face_nodes[1]
        vector[1] = face_nodes[0]-face_nodes[3]
        vector[2] = face_nodes[1]-face_nodes[3] # Intersection
        vector[3] = face_nodes[2]-face_nodes[3]
        vector[4] = face_nodes[2]-face_nodes[1]

        for i in range (5):
            norm[i] = np.linalg.norm(vector[i])

        semi_perimeter1 = (norm[0]+norm[1]+norm[2])/2
        semi_perimeter2 = (norm[3]+norm[4]+norm[2])/2

        area1 = np.sqrt(semi_perimeter1*(semi_perimeter1-norm[0])*(semi_perimeter1-norm[1])*(semi_perimeter1-norm[2]))
        area2 = np.sqrt(semi_perimeter2*(semi_perimeter2-norm[3])*(semi_perimeter2-norm[4])*(semi_perimeter2-norm[2]))

        quadrilateral_area = area1 + area2
        return quadrilateral_area

    def teste():
        print("Entrou")
        pass
