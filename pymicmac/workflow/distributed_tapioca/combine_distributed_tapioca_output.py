#!/usr/bin/python
import argparse
import os
from pymicmac import utils_execution


def run(inputFolder, outputFolder):
    """
    Runs Tapioca command.

    :param param1: inputFolder
    :param param2: outputFolder
    :returns: None
    """
    if os.path.isdir(outputFolder):
        raise Exception(outputFolder + ' already exists!')
    os.makedirs(outputFolder)

    for tapiocaCommandId in os.listdir(inputFolder):
        tapiocaCommandIdAbsPath = inputFolder + '/' + tapiocaCommandId
        tapiocaCommandIdHomolAbsPath = tapiocaCommandIdAbsPath + '/Homol'
        if os.path.isdir(tapiocaCommandIdHomolAbsPath) and len(
                os.listdir(tapiocaCommandIdHomolAbsPath)):
            os.system(
                'cp -r ' +
                tapiocaCommandIdHomolAbsPath +
                '/* ' +
                outputFolder)
        else:
            print(
                'WARNING: could not find tie-points in ' +
                tapiocaCommandIdHomolAbsPath)


def argument_parser():
    """
    Defines argument menu.

    :returns: parser
    """

    description = "Combine Homol folders into single one. To be run after a distributed Tapioca"
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument(
        '-i',
        '--inputFolder',
        default='',
        help='Input folder with the subfolders for each distributed Tapioca command. This folder contains subfolders <i>_Tapioca and each subfolder contains a Homol folder',
        type=str,
        required=True)
    parser.add_argument(
        '-o',
        '--outputFolder',
        default='',
        help='Output folder',
        type=str,
        required=True)
    return parser


def main():
    """
    The main workflow function. Uses the parsed arguments.
    """
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.inputFolder, a.outputFolder)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
