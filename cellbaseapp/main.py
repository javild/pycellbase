__author__ = 'fjlopez'

import argparse
# import ..cellbasecore
import sys
import QueryCommandExecutor
import os

def main():

    parser = argparse.ArgumentParser(description='CellBase client 1.0')
    parser.add_argument('--type', nargs=1, type=str, required=True,
                        help='String indicating the type of data to be queried', metavar='T', dest='type')
    parser.add_argument('--method', nargs=1, type=str, required=True,
                        help='String indicating the method to be queried', metavar='M', dest='method')
    parser.add_argument('--id', nargs=1, type=str, required=False,
                        help='String indicating the id(s) to be queried (if needed)', metavar='I', dest='id')
    parser.add_argument('--conf', nargs=1, default=None, type=str,
                        required=False,
                        help='Path to a .json file containing CellBase client configuration (if needed)', metavar='I',
                        dest='conf')

    args = parser.parse_args()

    commandExecutor = QueryCommandExecutor.QueryCommandExecutor(args)
    if(commandExecutor<>None):
        try:
            commandExecutor.loadCellBaseConfiguration()
            commandExecutor.execute()
        except Exception, e:
            print "Error loading CellBase configuration"
            print e.message
            sys.exit(1)

if __name__=='__main__':
    main()

