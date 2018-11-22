import configparser as cp
import pdb

def readConfig(configInput = "msCoarse.ini"):


    configInput = 'lololita'
    configFile = cp.ConfigParser()
    try:
        configFile.read(configInput)
    except:
        print("Não foi possivel ler o arquivo: "+configInput)
    return configFile


    #pdb.set_trace()
