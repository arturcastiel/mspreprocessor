
import yaml
# from yaml import load, dump


file = open('read_file.card', 'r')
stream = file.read()

bob = yaml.load_all(stream)


for i in bob:
    print(i)