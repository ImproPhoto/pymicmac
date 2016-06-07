#!/usr/bin/python
import sys, os, shutil
from pymicmac import utils_execution

xmlTapiocaFile = sys.argv[1]
imageListFile = xmlTapiocaFile + '.list'
gwd = sys.argv[2]

i = os.path.basename(xmlTapiocaFile).split('_')[0]
listImages = open(imageListFile,'r').read().split('\n')

lwd = sys.argv[3] + '/' + i 

shutil.rmtree(lwd, True)
os.makedirs(lwd)

os.chdir(lwd)

for image in listImages:
    if image != '':
        os.system('cp ' + gwd + '/' + image + ' .')

os.system('cp ' + xmlTapiocaFile + ' .')
command = 'mm3d Tapioca File ' + os.path.basename(xmlTapiocaFile) + ' -1'
utils_execution.executeCommandMonitor('Tapioca', command, lwd, False)

gOutputDir = gwd + '/MultiHomol'
try:
    os.makedirs(gOutputDir)
except OSError:
    print("Skipping creation of %s because it exists already." % gOutputDir)

os.system('cp Tapioca.log ' + gOutputDir + '/Tapioca_' + i + '.log')
os.system('cp Tapioca.mon ' + gOutputDir + '/Tapioca_' + i + '.mon')
os.system('cp Tapioca.mon.disk ' + gOutputDir + '/Tapioca_' + i + '.mon.disk')

os.system('cp -r Homol ' + gOutputDir + '/Homol_' + i)

os.system('rm -r ' + lwd)
