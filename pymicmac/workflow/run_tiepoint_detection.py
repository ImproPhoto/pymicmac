#!/usr/bin/python
import argparse, os
from pymicmac import utils_execution

def run(tapiocaOptions, onlyShowCommands):
    # Run Tapioca command
    command = 'mm3d Tapioca ' + tapiocaOptions
    mountPoint = os.getcwd()
    utils_execution.executeCommandMonitor('Tapioca', command, mountPoint, onlyShowCommands)


def argument_parser():
   # define argument menu
    description = "Runs Tapioca command in MicMac which generate the tie-points (this python script also monitors CPU, MEM and disk usage)"
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('--tapiocaOptions',default='', help='Options to invoke Tapioca, for example "File GrapheHom.xml -1"', type=str, required=True)
    parser.add_argument('--onlyShowCommands', default=False, help='Only shows the commands and does not execute them', action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.tapiocaOptions, a.onlyShowCommands)
    except Exception as e:
        print(e)
