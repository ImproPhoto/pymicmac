#!/usr/bin/python
import sys, os, shutil
from lxml import etree
from pymicmac import utils_execution

# Parse the parameters
configFile = sys.argv[1]
commandIndex = sys.argv[2]
dataDirAbsPath = sys.argv[3]
remoteExeDir = sys.argv[4]
localOutDirAbsPath = sys.argv[5]

# Read the command information from the XML and the provided index
if not os.path.isfile(configFile):
    raise Exception(configFile + " could not be found!")
e = etree.parse(open(configFile)).getroot()
c = e.xpath("//id[starts-with(text(),'" + commandIndex + "_')]/parent::*")[0]
commandId = c.find("id").text.strip()
command = c.find("command").text.strip()
imagesListFile = c.find("images").text.strip()
requiredElements= c.find("require").text.strip().split()
outputElements = c.find("output").text.strip().split()
print("CommandId: " + commandId)
print("Command: " + command)
print("Images list file: " + imagesListFile)
print("Required: " + ' '.join(requiredElements))
print("Output: " + ' '.join(outputElements))

# Check image list file can be accesses
imageListFileAbsPath = dataDirAbsPath + '/' + imagesListFile
if not os.path.isfile(imageListFileAbsPath):
    raise Exception(imageListFileAbsPath + " could not be found!")
listImages = open(imageListFileAbsPath,'r').read().split('\n')

# Create a local working directory using the specified remoteExeDir
lwd = remoteExeDir + '/' + commandId
shutil.rmtree(lwd, True)
os.makedirs(lwd)
# Change directory to be in the local working dir
os.chdir(lwd)

# Create a output directory in the shared folder to copy back the results
commandLocalOutDirAbsPath = localOutDirAbsPath + '/' + commandId
shutil.rmtree(commandLocalOutDirAbsPath, True)
os.makedirs(commandLocalOutDirAbsPath)

# Copy all the images from the data directory (in the shared folder) to the local one
for image in listImages:
    if image != '':
        imageAbsPath = dataDirAbsPath + '/' + image
        if os.path.isfile(imageAbsPath):
            os.system('cp ' + imageAbsPath + ' .')
        else:
            raise Exception(imageAbsPath + " could not be found!")
# Copy other required files and folders in the data directory
for requiredElement in requiredElements:
    requiredElementAbsPath =  dataDirAbsPath + '/' + requiredElement
    if os.path.isfile(requiredElementAbsPath):
        os.system('cp ' + requiredElementAbsPath + ' .')
    elif os.path.isdir(requiredElementAbsPath):
        os.system('cp -r ' + requiredElementAbsPath + ' .')
    else:
        raise Exception(requiredElementAbsPath + " could not be found!")

# Run the execution of the command (which includes cpu, mem and disk monitoring)
(logFile, monitorFile, monitorDiskFile) = utils_execution.executeCommandMonitor(commandId, command, lwd, False)

# Copy the monitor files back to the output dir in the shared folder
for f in (logFile, monitorFile, monitorDiskFile):
    if os.path.isfile(f):
        os.system('cp ' + f + ' ' + commandLocalOutDirAbsPath)
    else:
        raise Exception(f + " could not be found!")    
# Copy other output files and folders back to the output dir in the shared folder
for outputElement in outputElements:
    if os.path.isfile(outputElement):
        os.system('cp ' + outputElement + ' ' + commandLocalOutDirAbsPath)
    elif os.path.isdir(outputElement):
        os.system('cp -r ' + outputElement + ' ' + commandLocalOutDirAbsPath)
    else:
        raise Exception(outputElement + " could not be found!")

# Clean the local working dir
os.system('rm -r ' + lwd)
