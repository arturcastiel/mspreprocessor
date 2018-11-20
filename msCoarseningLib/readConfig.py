import configparser as cp
import pdb

def readConfig(configInput = "msCoarse.ini"):
    configFile = cp.ConfigParser()
    configFile.read(configInput)
    return configFile


    #pdb.set_trace()
