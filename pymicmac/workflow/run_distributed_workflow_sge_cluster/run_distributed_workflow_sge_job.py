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
e = etree.parse(configFile).getroot()
c = e.xpath("//id[starts-with(text(),'" + commandIndex + "_')]/parent::*")[0]
commandId = c.find("id").text.strip()
command = c.find("command").text.strip()
imagesListFile = c.find("images").text.strip()
requiredElements= c.find("require").text.strip().split()
outputElements = c.find("output").text.strip().split()

configFileAbsPath = dataDirAbsPath + '/' + configFile
imageListFileAbsPath = dataDirAbsPath + '/' + imagesListFile

listImages = open(imageListFileAbsPath,'r').read().split('\n')

lwd = remoteExeDir + '/' + commandId

shutil.rmtree(lwd, True)
os.makedirs(lwd)

os.chdir(lwd)

commandLocalOutDirAbsPath = localOutDirAbsPath + '/' + commandId
os.makedirs(commandLocalOutDirAbsPath)

for image in listImages:
    if image != '':
        os.system('cp ' + dataDirAbsPath + '/' + image + ' .')

for requiredElement in requiredElements:
    requiredElementAbsPath =  dataDirAbsPath + '/' + requiredElement
    if os.path.isfile(requiredElementAbsPath):
        os.system('cp ' + requiredElementAbsPath + ' .')
    elif os.path.isdir(requiredElementAbsPath):
        os.system('cp -r ' + requiredElementAbsPath + ' .')
    else:
        raise Exception(requiredElementAbsPath + " could not be found!")

utils_execution.executeCommandMonitor(commandId, command, lwd, False)

os.system('cp ' + commandId + '.log ' + commandLocalOutDirAbsPath)
os.system('cp ' + commandId + '.mon ' + commandLocalOutDirAbsPath)
os.system('cp ' + commandId + '.mon.disk ' + commandLocalOutDirAbsPath)

for outputElement in outputElements:
    if os.path.isfile(outputElement):
        os.system('cp ' + outputElement + ' ' + commandLocalOutDirAbsPath)
    elif os.path.isdir(requiredElementAbsPath):
        os.system('cp -r ' + outputElement + ' ' + commandLocalOutDirAbsPath)
    else:
        raise Exception(outputElement + " could not be found!")

os.system('rm -r ' + lwd)
