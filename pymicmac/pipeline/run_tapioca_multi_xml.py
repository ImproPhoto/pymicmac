#!/usr/bin/python
import argparse, glob, os
from pymicmac import utils_execution

def run(inputFolder, tapiocaOptions, mountPoint, onlyPrint):
    xmlFiles = glob.glob(inputFolder + '/*xml')

    for xmlFile in xmlFiles:
        # Run Tapioca command
        i = os.path.basename(xmlFile).split('_')[0]
        listImages = open(xmlFile + '.list','r').read().split('\n')
        for image in listImages:
            if image != '':
                print('cp ' + image + ' to local')
        print('cp ' + xmlFile + ' to local')
        command = 'mm3d Tapioca ' + tapiocaOptions.replace('[XML]', xmlFile)
        utils_execution.executeCommandMonitor('Tapioca', command, mountPoint, True)
        print('cp local Homol to shared MultiHomol/Homol_' + i)

def argument_parser():
   # define argument menu
    description = ""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--inputFolder',default='', help='', type=str, required=True)
    parser.add_argument('--tapiocaOptions',default='', help='Keyword [XML] will be replaced', type=str, required=True)
    parser.add_argument('--mountPoint',default='', help='', type=str, required=True)
    parser.add_argument('--onlyPrint', default=False, action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.inputFolder, a.tapiocaOptions, a.mountPoint, a.onlyPrint)
    except Exception as e:
        print(e)
