 #!/usr/bin/python
import os,time,stat,subprocess,shutil,glob
from pymicmac.monitor import monitor_cpu_mem_disk

def executeCommandMonitor(commandName, command, diskPath, onlyPrint=False):
    if onlyPrint:
        print(command)
        return

    # Define the names of the script that executes the command, the log file and the monitor file
    eFileName = commandName + '.sh'
    logFile = commandName + '.log'
    monitorLogFileName = commandName + '.mon'

    # Create script for command execution
    eFile = open(eFileName, 'w')
    eFile.write('#!/bin/bash\n')
    eFile.write(command  + ' >> ' + logFile + ' 2>&1')
    eFile.close()

    #Give execution rights
    os.chmod(eFileName, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    # Run the tool that executes the command with the monitoring of CPU and MEM
    monitor_cpu_mem_disk.run('./' + eFileName, monitorLogFileName, diskPath)

def getSize(absPath):
    (out,err) = subprocess.Popen('du -sb ' + absPath, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    try:
        return int(out.split()[0])
    except:
        return -1

def initPipelineFolder(pipelineName, imageFormat, itemsToLink):
    pwd = os.getcwd()

    # Recreate directory for this pipeline run
    shutil.rmtree(pipelineName, True)
    os.makedirs(pipelineName)

    #Create links of all images in the pipeline folder
    images = glob.glob('*.' + imageFormat)
    os.chdir(pipelineName)
    for image in images:
        os.symlink('../' + image, image)

    for itemToLink in itemsToLink:
        #Create link
        if os.path.isfile('../' + itemToLink) or os.path.isdir('../' + itemToLink):
            os.symlink('../' + itemToLink , itemToLink)
        else:
            raise Exception('../' + itemToLink + ' does not exist!')

    os.chdir(pwd)

def apply_argument_parser(argumentsParser, options=None):
    """ Apply the argument parser. """
    if options is not None:
        args = argumentsParser.parse_args(options)
    else:
        args = argumentsParser.parse_args()
    return args
