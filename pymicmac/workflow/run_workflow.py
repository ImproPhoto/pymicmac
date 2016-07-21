 #!/usr/bin/python
import os, argparse
from lxml import etree
from pymicmac import utils_execution

def run(dataDir, exeDir, configFile, onlyShowCommands, resume):
    cwd = os.getcwd()
    dataAbsPath = os.path.abspath(dataDir)
    executionFolderAbsPath = os.path.abspath(exeDir)

    if dataAbsPath == executionFolderAbsPath:
        raise Exception('Execution folder must be different than the data directory')

    # Read configuration of MicMac commands to execute
    e = etree.parse(configFile).getroot()
    mmComponents = e.findall('Component')

    # Initialize execution folder (i.e. create links)
    elements = []
    for mmComponent in mmComponents:
        typeToLinkComponent = mmComponent.find("require")
        if typeToLinkComponent != None:
            elements += typeToLinkComponent.text.strip().split()
        typeToLinkComponent = mmComponent.find("requirelist")
        if typeToLinkComponent != None:
            elements += utils_execution.getRequiredList(typeToLinkComponent.text.strip())
    utils_execution.initExecutionFolder(dataAbsPath, executionFolderAbsPath, elements, resume)

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

    # Change directory to initial folder
    os.chdir(cwd)

def argument_parser():
   # define argument menu
    description = "Runs a workflow with several commands specified by a Workflow XML configuration file. For each executed command there is monitoring of used CPU/MEM/disk."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--dataDir',default='', help='Data directory that contains all the required data (if using relative paths in <require> and <requirelist) in the Workflow XML configuration file, those path will be relative to the data directory specified with this option)', type=str, required=True)
    parser.add_argument('-c', '--configFile',default='', help='Workflow XML configuration file with the several commands.', type=str, required=True)
    parser.add_argument('-e', '--exeDir',default='', help='Execution folder path. The execution of the workflow will be done in a folder where links to required data will be made.', type=str, required=True)
    parser.add_argument('--onlyShowCommands', default=False, help='If enabled, it does not execute the initialization of the execution folder and it only shows the commands and does not execute them [default is disabled]', action='store_true')
    parser.add_argument('--resume', default=False, help='If enabled, it does not raise exception if the execution folder exists. This is useful when you want to redo parts of a workflow. If you use this option be sure to update the <require> and <requirelist> accordingly to avoid trying to link data that is already in the execution folder [default is disabled]', action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.dataDir, a.exeDir, a.configFile, a.onlyShowCommands, a.resume)
    except Exception as e:
        print(e)
