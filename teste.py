#
# import yaml
# # from yaml import load, dump
#
#
# file = open('read_file.card', 'r')
# stream = file.read()
#
# bob = yaml.load_all(stream)
#
#
# for i in bob:
#     print(i)

import pdb

class my_decorator(object):

    def __init__(self, f):
        print("inside my_decorator.__init__()")
        self.fun = f
        self.teste = 10
        #return f(num) # Prove that function definition has completed

    def __call__(self,num):
        print("inside my_decorator.__call__()")
        return self.fun(num)

    def __getitem__(self, item):
        print("inside my_decorator.__call__()")
        return item

@my_decorator
def aFunction(x):
    return x*x

pdb.set_trace()
print("Finished decorating aFunction()")

