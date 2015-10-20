__author__ = 'fjlopez'

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # Adds pycellbase root dir to the PYTHONPATH

from cellbasecore import CellBaseConfiguration
import CellBaseClient

class QueryCommandExecutor:

    PATH = "/cellbase/webservices/rest/"

    def __init__(self, queryCommandOptions):
        self.queryCommandOptions = queryCommandOptions
        self.configFile = queryCommandOptions.conf
        self.configuration = None

    def loadCellBaseConfiguration(self):
        if(self.configFile!=None):
            self.configuration = CellBaseConfiguration.CellBaseConfiguration(self.configFile)
        else:
            self.configuration = CellBaseConfiguration.CellBaseConfiguration(
                os.path.dirname(CellBaseConfiguration.CellBaseConfiguration.__file__)+"/resources/configuration.json")

    def execute(self):
        checkParameters()
        if (":" in self.url):
            hostAndPort = self.url.split(":")
            self.url = hostAndPort[0]
            self.port = int(hostAndPort[1])
            cellBaseClient = CellBaseClient.CellBaseClient(self.url, self.port, QueryCommandExecutor.PATH,
                                                self.configuration.getVersion(), self.species)
        else:
            cellBaseClient = CellBaseClient.CellBaseClient(self.url, self.port, QueryCommandExecutor.PATH,
                                                           self.configuration.getVersion(), self.species)
        print(cellBaseClient.get(self.type, self.method, self.id))

