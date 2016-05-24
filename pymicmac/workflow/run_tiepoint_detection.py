#!/usr/bin/python
import argparse
from pymicmac import utils_execution

def run(tapiocaOptions, mountPoint, onlyPrint):
    # Run Tapioca command
    command = 'mm3d Tapioca ' + tapiocaOptions
    utils_execution.executeCommandMonitor('Tapioca', command, mountPoint, onlyPrint)


def argument_parser():
   # define argument menu
    description = ""
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('--tapiocaOptions',default='', help='', type=str, required=True)
    parser.add_argument('--mountPoint',default='', help='', type=str, required=True)
    parser.add_argument('--onlyPrint', default=False, action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.tapiocaOptions, a.mountPoint, a.onlyPrint)
    except Exception as e:
        print(e)
