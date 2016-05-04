#!/usr/bin/python
import argparse, os

def run(inputFolder):
    # Run Tapioca command
    if os.path.isdir('Homol'):
        raise Exception('Homol already exists!')
    os.makedirs('Homol')

    for e in os.listdir(inputFolder):
        os.system('cp -r ' + inputFolder + '/' + e + '/* ' + 'Homol' )

def argument_parser():
   # define argument menu
    description = ""
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('--inputFolder',default='', help='A folder containing all the homol folders to be combined', type=str, required=True)
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.inputFolder)
    except Exception as e:
        print(e)
