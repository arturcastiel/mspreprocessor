import time
import numpy as np
from pymoab import core, types, rng

mbcore = core.Core()

num_elem_z = 1
num_elem_y = 1
num_elem_x = 1
dx, dy, dz = 1., 1., 1.

# Definindo array com as coordenadas da malha
vertex_coords = np.array([]) # Inicializando vetor com as coordenadas dos vértices
for k in range (num_elem_z+1):
    for j in range(num_elem_y+1):
        for i in range(num_elem_x+1):
            vertex_coords = np.append(vertex_coords, [i*dx, j*dy, k*dz])

vertex_handles = mbcore.create_vertices(vertex_coords)

coord = np.zeros([8,3],dtype='float64')
j = 0

for i in range (8):
    coord[i] = [vertex_coords[i+j], vertex_coords[i+j+1], vertex_coords[i+j+2]]
    j = j+2
'''
temp = np.zeros([1,3], dtype='float64')

temp[0] = coord[0]
coord[0] = coord[1]
coord[1] = coord[3]
coord[3] = coord[2]
coord[2] = temp

temp[0] = coord[4]
coord[4] = coord[5]
coord[5] = coord[7]
coord[7] = coord[6]
coord[6] = temp
'''

# Method TH
inicio1 = time.time()
vector = np.cross(((coord[7]-coord[1])+(coord[6]-coord[0])), (coord[7]-coord[2]))
vector = np.dot(vector, (coord[3]-coord[0]))

vector2 = np.cross((coord[6]-coord[0]), (coord[7]-coord[2])+(coord[5]-coord[0]))
vector2 = np.dot(vector2,(coord[7]-coord[4]))

vector3 = np.cross((coord[7]-coord[1]), (coord[5]-coord[0]))
vector3 = np.dot(vector3, ((coord[7]-coord[4])+(coord[3]-coord[0])))
final1 = time.time()
volume = (vector+vector2+vector3)/12

# Method LD
inicio2 = time.time()
vetor = np.cross((coord[7]-coord[0]), (coord[1]-coord[0]))
vetor = np.dot(vetor, (coord[3]-coord[5]))

vetor2 = np.cross((coord[7]-coord[0]), (coord[4]-coord[0]))
vetor2 = np.dot(vetor2,(coord[5]-coord[6]))

vetor3 = np.cross((coord[7]-coord[0]), (coord[2]-coord[0]))
vetor3 = np.dot(vetor3, (coord[6]-coord[3]))
final2 = time.time()

volume2 = (vetor+vetor2+vetor3)/6

print(final1-inicio1)
print(final2-inicio2)
