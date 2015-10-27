__author__ = 'fjlopez'


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # Adds pycellbase root dir to the PYTHONPATH

import argparse
import QueryCommandExecutor


def main():

    parser = argparse.ArgumentParser(description='CellBase client 1.0')
    parser.add_argument('--type', nargs=1, type=str, required=True,
                        help='String indicating the type of data to be queried', metavar='T', dest='type')
    parser.add_argument('--method', nargs=1, type=str, required=True,
                        help='String indicating the method to be queried', metavar='M', dest='method')
    parser.add_argument('--id', nargs=1, type=str, required=False,
                        help='String indicating the id(s) to be queried (if needed)', metavar='I', dest='id')
    parser.add_argument('--species', nargs=1, default="hsapiens", type=str, required=False,
                        help='String indicating the species to query', metavar='S', dest='species')
    parser.add_argument('--options', nargs=1, type=str, required=False,
                        help='String with a list of &-separated filtering options. For example: source=clinvar&skip=10&limit=200', metavar='O', dest='options')
    parser.add_argument('--conf', nargs=1, default=None, type=str,
                        required=False,
                        help='Path to a .json file containing CellBase client configuration (if needed)', metavar='I',
                        dest='conf')

    args = parser.parse_args()

    commandExecutor = QueryCommandExecutor.QueryCommandExecutor(args)
    if(commandExecutor!=None):
        try:
            commandExecutor.loadCellBaseConfiguration()
            commandExecutor.execute()
        except Exception as e:
            print("Error loading CellBase configuration")
            print(e.message)
            sys.exit(1)

if __name__=='__main__':
    main()

