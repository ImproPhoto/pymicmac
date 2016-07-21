 #!/usr/bin/python
import os,time,stat,subprocess,shutil,glob
from pymicmac.monitor import monitor_cpu_mem_disk
from lxml import etree

def readGCPXMLFile(xmlFile):
    gcpsXYZ = {}
    cpsXYZ = {}

    if not os.path.isfile(xmlFile):
        raise Exception('ERROR: ' + xmlFile + ' not found')

    e = etree.parse(xmlFile).getroot()
    for p in e.getchildren():
        gcp = p.find('NamePt').text
        fields = p.find('Pt').text.split()
        incertitude = p.find('Incertitude').text

        x = float(fields[0])
        y = float(fields[1])
        z = float(fields[2])
        if incertitude.count('-1'):
            cpsXYZ[gcp] = (x, y, z)
        else:
            gcpsXYZ[gcp] = (x, y, z)
    return (gcpsXYZ, cpsXYZ)

def executeCommandMonitor(commandId, command, diskPath, onlyPrint=False):
    # Define the names of the script that executes the command, the log file and the monitor file
    # eFileName = commandId + '.sh'
    logFileName = commandId + '.log'
    monitorLogFileName = commandId + '.mon'
    monitorDiskLogFileName = commandId + '.mon.disk'

    #Remove log file if already exists
    for f in (logFileName,monitorLogFileName,monitorDiskLogFileName):
        if os.path.isfile(f):
            os.system('rm ' + f)

    if onlyPrint:
        print(command)
        os.system('touch ' + logFileName)
        os.system('touch ' + monitorLogFileName)
        os.system('touch ' + monitorDiskLogFileName)
    else:
        monitor_cpu_mem_disk.run(command, logFileName, monitorLogFileName, monitorDiskLogFileName, diskPath)
        # TODO: if execution folder is in different file system that source data, right now we only monitor raw data usage
    return (logFileName,monitorLogFileName,monitorDiskLogFileName)

def getSize(absPath):
    (out,err) = subprocess.Popen('du -sb ' + absPath, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    try:
        return int(out.split()[0])
    except:
        return -1

def initExecutionFolder(dataDir, executionFolder, mmComponents):
    # Create directory for this execution
    executionFolderAbsPath = os.path.abspath(executionFolder)
    if os.path.exists(executionFolderAbsPath):
        raise Exception(executionFolder + ' already exists!')
    os.makedirs(executionFolderAbsPath)

    # Create links for the files/folder specifed in require and requirelist XML
    for mmComponent in mmComponents:
        elements = []
        typeToLinkComponent = mmComponent.find("require")
        if typeToLinkComponent != None:
            elements += typeToLinkComponent.text.strip().split()
        typeToLinkComponent = mmComponent.find("requirelist")
        if typeToLinkComponent != None:
            elements += getRequiredList(typeToLinkComponent.text.strip())
        for element in elements:
            if element.endswith('/'):
                element = element[:-1]
            if element.startswith('/'):
                elementAbsPath = element
            else:
                elementAbsPath = dataDir + '/' + element
            if os.path.isfile(elementAbsPath) or os.path.isdir(elementAbsPath):
                os.symlink(elementAbsPath , os.path.join(executionFolderAbsPath, os.path.basename(elementAbsPath)))
            else:
                raise Exception(element + ' does not exist!')

def getRequiredList(requiredListFile):
    required = []
    if not os.path.isfile(requiredListFile):
        raise Exception(requiredListFile + ' does not exist!')
    for line in open(requiredListFile, 'r').read().split('\n'):
        if line != '':
            required.append(line)
    return required

def apply_argument_parser(argumentsParser, options=None):
    """ Apply the argument parser. """
    if options is not None:
        args = argumentsParser.parse_args(options)
    else:
        args = argumentsParser.parse_args()
    return args
