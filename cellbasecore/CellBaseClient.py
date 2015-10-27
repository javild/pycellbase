
__author__ = 'fjlopez'

import json
import urllib2

class CellBaseClient:

    def __init__(self, host, port, path, version, species):
        self.host = host
        self.port = port
        self.path = path
        self.version = version
        self.species = species

    def get(self, subtype, method, id, options):
        return json.loads(urllib2.urlopen(self.buildUrl(subtype,method,id,options)).read())

    def buildUrl(self, subtype, method, id, options):
        self.url = "http://"+self.host+":"+str(self.port)+self.path+self.version+"/"+self.species+"/"+\
                   CellBaseClient.TYPES[subtype]+"/"+subtype
        if(id!=None):
            self.url += "/"+id
        self.url += "/"+method
        if(options!=None):
            self.url += "?"+options



