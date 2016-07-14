 #!/usr/bin/python
import os, argparse
from lxml import etree
from pymicmac import utils_execution

def run(images, name, configFile, onlyShowCommands, noInit):
    rootPath = os.getcwd()
    executionFolderAbsPath = os.path.abspath(name)

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
        componentName = mmComponent.find("name").text.strip()
        componentOptions = mmComponent.find("options").text.strip()
        command = 'mm3d ' + componentName + ' ' + componentOptions
        utils_execution.executeCommandMonitor(componentName, command, rootPath, onlyShowCommands)

        if componentName == "OriRedTieP":
            # From now one we use as Homol folder the one we just created
            if not onlyShowCommands:
                if not os.path.isdir('HomolTiePRed'):
                    raise Exception('OriRedTieP did not generate a folder with reduced set of points!')
                os.system('rm Homol')
                os.system('mv HomolTiePRed Homol')
        if componentName == "RedTieP":
            if "ExpSubCom=1" in componentOptions:
                noodlesNumProc = mmComponent.find("noodlesParallel").text.strip()
                noodlesExePath = os.path.abspath(os.path.join(os.path.realpath(__file__),'../../noodles/noodles_exe_parallel.py'))
                command = 'python ' + noodlesExePath + ' -j ' + str(noodlesNumProc) + ' subcommands.json RedTieP_logs'
                utils_execution.executeCommandMonitor('Noodles', command, rootPath, onlyShowCommands)
            # From now one we use as Homol folder the one we just created
            if not onlyShowCommands:
                if not os.path.isdir('Homol-Red'):
                    raise Exception('OriRedTieP did not generate a folder with reduced set of points!')
                os.system('rm Homol')
                os.system('mv Homol-Red Homol')

    # Change directory to root folder
    os.chdir(rootPath)

def argument_parser():
   # define argument menu
    description = "Runs a workflow with several MicMac commands specified by the XML configuration file. For each executed command there is monitoring of used CPU/MEM/disk."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--images',default='', help='File with list of images paths (one image per line)', type=str, required=True)
    parser.add_argument('-n', '--name',default='', help='Name of execution folder. The execution of the workflow will be done in a folder where links to required data will be made.', type=str, required=True)
    parser.add_argument('-c', '--configFile',default='', help='XML configuration file with the several commands', type=str, required=True)
    parser.add_argument('--onlyShowCommands', default=False, help='If enabled, it does not execute the initialization of the execution folder and it only shows the commands and does not execute them [default is disabled]', action='store_true')
    parser.add_argument('--noInit', default=False, help='If enabled, it does not run the initialization of the execution folder (creating it and making the links) [default is disabled]', action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(utils_execution.getImages(a.images), a.name, a.configFile, a.onlyShowCommands, a.noInit)
    except Exception as e:
        print(e)
