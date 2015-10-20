__author__ = 'fjlopez'

import json

class CellBaseConfiguration(dict):
    def __init__(self, configFileName):
        fdw = open(configFileName)
        dictionaryString = fdw.readlines(fdw)
        fdw.close()
        dict.__init__(self, json.loads(dictionaryString))
