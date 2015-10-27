__author__ = 'fjlopez'

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # Adds pycellbase root dir to the PYTHONPATH

import string
from cellbasecore import CellBaseConfiguration,CellBaseClient
from cellbasecore.exceptions import InvalidQueryTypeException,InvalidQueryMethodException,InvalidQuerySpeciesException,InvalidQueryOptionsException

class QueryCommandExecutor:

    PATH = "/cellbase/webservices/rest/"
    ENABLEDQUERYTYPES = ["clinical","exon","gene","variant","chromosome","meta","protein","snp","tf","id"]
    ENABLEDQUERYMETHODS = {"clinical" : set(["all","help","listAcc","phenotype-gene"]),
                           "exon" : set(["stats","first","help","model","count","aminos","info","region","sequence","transcript"]),
                           "gene" : set(["tfbs","biotype","count","first","help","list","model","stats","clinical","info","mirna_target","mutation","next","ppi","protein","snp","stats","all","transcript","count","first","fullinfo","function_prediction","gene","mutation","region","sequence","variation"]),
                           "genomic" : set(["all","help","list","model","ctyoband","info","size"]),
                           "meta" : set(["help","species","versions"]),
                           "protein" : set(["gene","help","model","fullinfo","all","info","name","reference","sequence","transcript"]),
                           "region" : set(["exon","help","model","clinical","conservation","conserved_region","cpg_island","cytoband","tfbs","gene","mutation","phenotype","regulatory","sequence","snp","structural_variation","transcript"]),
                           "snp" : set(["xref","consequence_types","count","first","help","model","sequence","phenotypes","regulatory","stats","info","next","phenotype","population_frequency","consequence_type"]),
                           "species" : set(["help","info"]),
                           "tf" : set(["annotation","help","tfbs"]),
                           "xref" : set(["id","help","model","contains","gene","info","snp","starts_with","xref"])
                           }
    ENABLEDQUERYSPECIES = {"hsapiens", "mmusculus", "drerio", "rnorvegicus", "ptroglodytes", "ggorilla", "pabelii", "mmulatta", "csabaeus", "sscrofa", "cfamiliaris", "ecaballus", "ocuniculus", "ggallus", "btaurus", "fcatus", "cintestinalis", "oaries", "olatipes", "ttruncatus", "lafricana", "cjacchus", "nleucogenys", "aplatyrhynchos", "falbicollis", "celegans", "dmelanogaster", "dsimulans", "dyakuba", "agambiae", "adarlingi", "nvectensis", "spurpuratus", "bmori", "aaegypti", "apisum", "scerevisiae", "spombe", "afumigatus", "aniger", "anidulans", "aoryzae", "foxysporum", "pgraminis", "ptriticina", "moryzae", "umaydis", "ssclerotiorum", "cneoformans", "ztritici", "pfalciparum", "lmajor", "ddiscoideum", "glamblia", "pultimum", "alaibachii", "athaliana", "alyrata", "bdistachyon", "osativa", "gmax", "vvinifera", "zmays", "hvulgare", "macuminata", "sbicolor", "sitalica", "taestivum", "brapa", "ptrichocarpa", "slycopersicum", "stuberosum", "smoellendorffii", "creinhardtii", "cmerolae"}



    def __init__(self, queryCommandOptions):
        self.queryCommandOptions = queryCommandOptions
        self.configFile = queryCommandOptions.conf
        self.configuration = None

    def loadCellBaseConfiguration(self):
        if(self.configFile!=None):
            self.configuration = CellBaseConfiguration.CellBaseConfiguration(self.configFile)
        else:
            self.configuration = CellBaseConfiguration.CellBaseConfiguration(
                os.path.dirname(CellBaseConfiguration.__file__)+"/resources/configuration.json")

    def execute(self):
        self.checkParameters()
        cellBaseClient = CellBaseClient.CellBaseClient("http://"+self.configuration.getHost(),
                                                       self.configuration.getPort(), QueryCommandExecutor.PATH,
                                                       self.configuration.getVersion(), self.species)
        print(cellBaseClient.get(self.type, self.method, self.id, self.options))

    def checkParameters(self):
        if(self.queryCommandOptions.type!=None and
                   self.queryCommandOptions.type.lower() in QueryCommandExecutor.ENABLEDQUERYTYPES):
            self.type = self.queryCommandOptions.type.lower()
        else:
            raise InvalidQueryTypeException.InvalidQueryTypeException(
                self.queryCommandOptions.type+" is not a valid query type. Please provide one of the following: {"+
                string.join(QueryCommandExecutor.ENABLEDQUERYTYPES, sep=", ")+"}")
        if(self.queryCommandOptions.method!=None and
                  self.queryCommandOptions.method.lower() in QueryCommandExecutor.ENABLEDQUERYMETHODS[self.queryCommandOptions.type]):
            self.method = self.queryCommandOptions.method.lower()
        else:
            raise InvalidQueryMethodException.InvalidQueryMethodException(
                self.queryCommandOptions.method+" is not a valid query method for type "+self.queryCommandOptions.type+". Please provide one of the following: {"+
                string.join(QueryCommandExecutor.ENABLEDQUERYMETHODS[self.queryCommandOptions.type], sep=", ")+"}")
        self.id = self.queryCommandOptions.id
        if(self.queryCommandOptions.species!=None and
                   self.queryCommandOptions.species.lower() not in QueryCommandExecutor.ENABLEDQUERYSPECIES):
            raise InvalidQuerySpeciesException.InvalidQuerySpeciesException(
                self.queryCommandOptions.species+" is not a valid species. Please provide one of the following: {"+
                string.join(QueryCommandExecutor.ENABLEDQUERYSPECIES, sep=", ")+"}")
        else:
            self.species = self.queryCommandOptions.species.lower()
        if(self.validQueryOptions(self.queryCommandOptions.options)):
            self.options = self.queryCommandOptions.options
        else:
            raise InvalidQueryOptionsException.InvalidQueryOptionsException(
                "Incorrect format provided for query options. Please, provide a list of &-separated filters. For example: source=clinvar&skip=10&limit=200")

    def validQueryOptions(self,optionsString):
        parts = optionsString.split("&")
        i = 0
        while(i<len(parts) and len(parts[i].split("="))==2):
            i += 1
        return i==len(parts)



