 #!/usr/bin/python
import os, argparse
from lxml import etree
from pymicmac import utils_execution

def run(name, extension, configFile, onlyShowCommands, noInit):
    rootPath = os.getcwd()

    mountPoint = rootPath

    e = etree.parse(configFile).getroot()
    mmComponents = e.findall('Component')

    #Gather a list of files/folders to link in the workflow folder
    toLink = ['Homol',]
    for mmComponent in mmComponents:
        typeToLinkComponent = mmComponent.find("toLink")
        if typeToLinkComponent != None:
            toLink.extend(typeToLinkComponent.text.strip().split())

    if not noInit:
        # Initialize workflow folder (i.e. create link of images, homol folder and other files required by processing)
        utils_execution.initPipelineFolder(name, extension, toLink)

    # Change directory to workflow folder
    os.chdir(name)

    for mmComponent in mmComponents:
        # Run component of workflow
        componentName = mmComponent.find("name").text.strip()
        componentOptions = mmComponent.find("options").text.strip()
        command = 'mm3d ' + componentName + ' ' + componentOptions
        utils_execution.executeCommandMonitor(componentName, command, mountPoint, onlyShowCommands)

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
                utils_execution.executeCommandMonitor('Noodles', command, mountPoint, onlyShowCommands)
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
    description = ""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n', '--name',default='Name of execution folder. The execution of the parameters estimation will be done in a folder where links to Homol folder and the images will be made.', help='', type=str, required=True)
    parser.add_argument('-e', '--extension',default='', help='Images format (example JPG). This is used to create links to all the images in the execution folder', type=str, required=True)
    parser.add_argument('-c', '--configFile',default='', help='XML configuration file with the several steps to perform the parameters estimation (this should at leat include a Tapas element or similar)', type=str, required=True)
    parser.add_argument('--onlyShowCommands', default=False, help='Only shows the commands and does not execute them', action='store_true')
    parser.add_argument('--noInit', default=False, action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.name, a.extension, a.configFile, a.onlyShowCommands, a.noInit)
    except Exception as e:
        print(e)
