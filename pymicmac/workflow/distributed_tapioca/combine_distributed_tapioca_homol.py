#!/usr/bin/python
import argparse, os
from pymicmac import utils_execution

def run(inputFolder, outputFolder):
    # Run Tapioca command
    if os.path.isdir(outputFolder):
        raise Exception(outputFolder + ' already exists!')
    os.makedirs(outputFolder)

    for tapiocaCommandId in os.listdir(inputFolder):
        tapiocaCommandIdAbsPath = inputFolder + '/' + tapiocaCommandId
        tapiocaCommandIdHomolAbsPath = tapiocaCommandIdAbsPath + '/Homol'
        if os.path.isdir(tapiocaCommandIdHomolAbsPath) and len(os.listdir(tapiocaCommandIdHomolAbsPath)):
            os.system('cp -r ' + tapiocaCommandIdAbsPath + '/* ' + outputFolder)
        else:
            print('WARNING: could not find tie-points in ' + tapiocaCommandIdHomolAbsPath)
            
def argument_parser():
   # define argument menu
    description = "Combine Homol folders into single one. To be run after a distributed Tapioca"
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-i','--inputFolder',default='', help='Input folder with the subfolders for each distributed Tapioca command. This folder contains subfolders <i>_Tapioca and each subfolder contains a Homol folder', type=str, required=True)
    parser.add_argument('-o','--outputFolder',default='', help='Output folder', type=str, required=True)
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.inputFolder, a.outputFolder)
    except Exception as e:
        print(e)
