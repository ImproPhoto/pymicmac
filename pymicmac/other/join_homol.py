#!/usr/bin/python
import argparse, os
from pymicmac import utils_execution

def run(inputFolder, outputFolder):
    # Run Tapioca command
    if os.path.isdir(outputFolder):
        raise Exception(outputFolder + ' already exists!')
    os.makedirs(outputFolder)

    for e in os.listdir(inputFolder):
        if os.path.isdir(inputFolder + '/' + e):
            os.system('cp -r ' + inputFolder + '/' + e + '/* ' + outputFolder)

def argument_parser():
   # define argument menu
    description = ""
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-i','--inputFolder',default='', help='A folder containing all the homol folders to be combined', type=str, required=True)
    parser.add_argument('-o','--outputFolder',default='', help='Output folder', type=str, required=True)
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.inputFolder, a.outputFolder)
    except Exception as e:
        print(e)
