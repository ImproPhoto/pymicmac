#!/usr/bin/python
import sys
import os
import argparse
from tabulate import tabulate
from pymicmac import utils_execution


def run(foldersNames):
    table = []
    header = ['#Name', 'NumIter', 'Res', 'Wor']

    for folderName in foldersNames.split(','):
        if folderName.endswith('/'):
            folderName = folderName[:-1]
        logFileName = folderName + '/Tapas.log'
        if os.path.isfile(logFileName):
            lines = open(logFileName, 'r').read().split('\n')
            residuals = []
            worsts = []
            c1 = 0
            for line in lines:
                if line.count('Residual = '):
                    c1 += 1
                    residuals.append(
                        line.split(';;')[0].replace(
                            '| |  Residual = ', ''))
                elif line.count(' Worst, Res '):
                    worsts.append(
                        line.split('for')[0].replace(
                            '| |  Worst, Res ', ''))
            if len(worsts) and len(residuals):
                table.append([folderName, str(c1), residuals[-1], worsts[-1]])
            else:
                table.append([folderName, '-', '-', '-'])
        else:
            table.append([folderName, '-', '-', '-'])

    print("##########################")
    print("Tapas last residuals/worts")
    print("##########################")
    print(tabulate(table, headers=header))
    print()


def argument_parser():
                 # define argument menu
    description = "Gets statistics of Tapas runs in one or more execution folders"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-f',
        '--folders',
        default='',
        help='Comma-separated list of execution folders where to look for the Tapas.log files',
        type=str,
        required=True)
    return parser


def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.folders)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
