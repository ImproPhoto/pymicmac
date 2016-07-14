#!/usr/bin/python
import sys, os, argparse
from tabulate import tabulate
from pymicmac import utils_execution

def run(foldersNames):
    header = ['#Name', 'CInit', 'Ini', 'CEnd', 'End']
    table = []
    for folderName in foldersNames.split(','):
        if folderName.endswith('/'):
            folderName = folderName[:-1]
        logFileName = folderName + '/RedTieP.log'
        logFolderName = folderName + '/RedTieP_logs'
        if os.path.isdir(logFolderName):
            lines = os.popen('cat ' + logFolderName + '/*').read().split('\n')
        elif os.path.isfile(logFileName):
            lines = open(logFileName, 'r').read().split('\n')
        inits = []
        ends = []
        c1 = 0
        c2 = 0
        for line in lines:
            if line.count('#InitialHomolPoints:'):
                c1+=1
                inits.append(int(line.split(' ')[0].split(':')[-1].replace('.','')))
            if line.count('#HomolPoints:'):
                c2+=1
                ends.append(int(line.split(' ')[1].split('=>')[-1].split('(')[0]))

        table.append([folderName, str(c1), str(sum(inits)), str(c2), str(sum(ends))])

    print("#################")
    print("RedTieP reduction")
    print("#################")
    print(tabulate(table, headers=header))

def argument_parser():
   # define argument menu
    description = "Gets statistics of RedTieP runs in one or more execution folders"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-f', '--folders',default='', help='Comma-separated list of execution folders where to look for the RedTieP.log files (or RedTieP_logs folders if RedTieP was executed with Noodels)', type=str, required=True)
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.folders)
    except Exception as e:
        print(e)
