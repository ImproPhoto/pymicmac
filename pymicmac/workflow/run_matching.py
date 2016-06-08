 #!/usr/bin/python
import os, argparse
from lxml import etree
from pymicmac import utils_execution

def run(name, orientation, configFile, onlyShowCommands):
    rootPath = os.getcwd()

    e = etree.parse(configFile).getroot()
    mmComponents = e.findall('Component')

    # Change directory to workflow folder
    os.chdir(name)

    for mmComponent in mmComponents:
        # Run component of workflow
        componentName = mmComponent.find("name").text.strip()
        componentOptions = mmComponent.find("options").text.strip()
        command = 'mm3d ' + componentName + ' ' + componentOptions
        utils_execution.executeCommandMonitor(componentName, command, rootPath, onlyShowCommands)

    # Change directory to root folder
    os.chdir(rootPath)

def argument_parser():
   # define argument menu
    description = ""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n', '--name',default='Name of execution folder. The name of the folder where the parameters where estimated. The matching will also be done in that folder', help='', type=str, required=True)
    parser.add_argument('-o', '--orientation',default='', help='Orientation (within the execution folder) to use for the matching (use MicMac naming convention, i.e. for example if folder is Ori-TapasOut, you need to specify only TapasOut)', type=str, required=True)
    parser.add_argument('-c', '--configFile',default='', help='XML configuration file with the several steps to perform the matching', type=str, required=True)
    parser.add_argument('--onlyShowCommands', default=False, help='Only shows the commands and does not execute them', action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.name, a.orientation, a.configFile, a.onlyShowCommands)
    except Exception as e:
        print(e)
