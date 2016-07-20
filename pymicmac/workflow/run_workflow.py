 #!/usr/bin/python
import os, argparse
from lxml import etree
from pymicmac import utils_execution

def run(images, exeDir, configFile, onlyShowCommands, noInit):
    cwd = os.getcwd()
    dataAbsPath = os.path.dirname(images[0])
    executionFolderAbsPath = os.path.abspath(exeDir)

    if dataAbsPath == executionFolderAbsPath:
        raise Exception('Execution folder must be different that the one with the images')

    # Read configuration of MicMac commands to execute
    e = etree.parse(configFile).getroot()
    mmComponents = e.findall('Component')

    # Initialize the execution folder
    if not noInit:
        # Initialize execution folder (i.e. create links)
        utils_execution.initExecutionFolder(images, executionFolderAbsPath, mmComponents)

    if not onlyShowCommands:
        # Change directory to execution folder
        os.chdir(executionFolderAbsPath)

    for mmComponent in mmComponents:
        # Run component of workflow
        commandId = mmComponent.find("id").text.strip()
        if commandId.count(' '):
            raise Exception('Command IDs cannot contain whitespaces!')
        command = mmComponent.find("command").text.strip()

        utils_execution.executeCommandMonitor(commandId, command, dataAbsPath, onlyShowCommands)

        if commandId == "OriRedTieP":
            # From now one we use as Homol folder the one we just created
            if not onlyShowCommands:
                if not os.path.isdir('HomolTiePRed'):
                    raise Exception('OriRedTieP did not generate a folder with reduced set of points!')
                os.system('rm Homol')
                os.system('mv HomolTiePRed Homol')
        if commandId == "RedTieP":
            if "ExpSubCom=1" in command:
                noodlesNumProc = mmComponent.find("noodlesParallel").text.strip()
                noodlesExePath = os.path.abspath(os.path.join(os.path.realpath(__file__),'../../noodles/noodles_exe_parallel.py'))
                command = 'python ' + noodlesExePath + ' -j ' + str(noodlesNumProc) + ' subcommands.json RedTieP_logs'
                utils_execution.executeCommandMonitor('Noodles', command, dataAbsPath, onlyShowCommands)
            # From now one we use as Homol folder the one we just created
            if not onlyShowCommands:
                if not os.path.isdir('Homol-Red'):
                    raise Exception('OriRedTieP did not generate a folder with reduced set of points!')
                os.system('rm Homol')
                os.system('mv Homol-Red Homol')

    # Change directory to initial folder
    os.chdir(cwd)

def argument_parser():
   # define argument menu
    description = "Runs a workflow with several MicMac commands specified by the XML configuration file. For each executed command there is monitoring of used CPU/MEM/disk."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--images',default='', help='File with list of images to consider (one image per line).', type=str, required=True)
    parser.add_argument('-c', '--configFile',default='', help='XML configuration file with the several commands.', type=str, required=True)
    parser.add_argument('-e', '--exe',default='', help='Execution folder path. The execution of the workflow will be done in a folder where links to required data will be made.', type=str, required=True)
    parser.add_argument('--onlyShowCommands', default=False, help='If enabled, it does not execute the initialization of the execution folder and it only shows the commands and does not execute them [default is disabled]', action='store_true')
    parser.add_argument('--noInit', default=False, help='If enabled, it does not run the initialization of the execution folder (creating it and making the links) [default is disabled]', action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(utils_execution.getImages(a.images), a.exe, a.configFile, a.onlyShowCommands, a.noInit)
    except Exception as e:
        print(e)
