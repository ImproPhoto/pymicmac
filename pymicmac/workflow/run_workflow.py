#!/usr/bin/python
import argparse
from pycoeman.seqcommands import run_seqcommands_local
from pymicmac import utils_execution


def argument_parser():
    """
    Define argument menu.

    :returns: parser
    """
    description = "Run a set of MicMac commands sequentially (one after the other). The commands are specified by a Worflow XML configuration file. During the execution of each command there is monitoring of the used CPU/MEM/disk by the system."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-d',
        '--dataDir',
        default='',
        help='Data directory that contains all the required data (if using relative paths in <require> and <requirelist) in the XML configuration file, those path will be relative to the data directory specified with this option)',
        type=str,
        required=True)
    parser.add_argument(
        '-c',
        '--configFile',
        default='',
        help='Worflow XML configuration file with the several commands.',
        type=str,
        required=True)
    parser.add_argument(
        '-e',
        '--exeDir',
        default='',
        help='Execution folder path. The execution of the commands will be done in a folder where links to required data will be made.',
        type=str,
        required=True)
    parser.add_argument(
        '--onlyShowCommands',
        default=False,
        help='If enabled, it does not execute the initialization of the execution folder (create links) and it only shows the commands without execute them [default is disabled]',
        action='store_true')
    parser.add_argument(
        '--resume',
        default=False,
        help='If enabled, it does not raise exception if the execution folder exists. This is useful when you want to redo some of the commands. If you use this option be sure to update the <require> and <requirelist> accordingly to avoid trying to link data that is already in the execution folder [default is disabled]',
        action='store_true')
    return parser


def main():
    """
    The main workflow function. Uses the parsed arguments.

    """
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run_seqcommands_local.run(
            a.dataDir,
            a.exeDir,
            a.configFile,
            a.onlyShowCommands,
            a.resume)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
