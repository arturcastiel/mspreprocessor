print('msCoarsening eoutines inicializado com sucesso')
from configparser import ConfigParser

class msCoarsening:
    def __init__(self,fineMsh):

        parser = ConfigParser()
        self.a = parser.read('msCoarse.ini')

        print('hello')
