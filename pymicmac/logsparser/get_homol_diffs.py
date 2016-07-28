 #!/usr/bin/python
import sys, numpy, argparse
from tabulate import tabulate
from pymicmac import utils_execution

def run(originalHomol, compareHomols):
    table = []
    header = ['#Name', 'Homol dec']

    rootHomolSize = utils_execution.getSize(originalHomol)

    compareHomols = compareHomols.split(',')

    for compareHomol in compareHomols:
        homolSize = utils_execution.getSize(compareHomol)
        pattern = "%0.4f"
        if homolSize > 0:
            table.append([compareHomol, pattern % ((homolSize/rootHomolSize))])
        else:
            table.append([compareHomol, '-'])

    print("###########")
    print("Ratio Homol")
    print("###########")
    print(tabulate(table, headers=header))
    print()

def argument_parser():
   # define argument menu
    description = "Gets statistics of comparing Homol folder in different execution folders"
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-o','--original',default='', help='Original Homol folder', type=str, required=True)
    parser.add_argument('-c','--compare',default='', help='Comma-separated Homol folder to compare', type=str, required=True)
    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.original, a.compare)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
