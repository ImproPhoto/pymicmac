#!/usr/bin/python
import os
import subprocess
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


def getSize(absPath):
    (out, _) = subprocess.Popen('du -sb ' + absPath, shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    try:
        return int(out.split()[0])
    except BaseException:
        return -1


def apply_argument_parser(argumentsParser, options=None):
    """ Apply the argument parser. """
    if options is not None:
        args = argumentsParser.parse_args(options)
    else:
        args = argumentsParser.parse_args()
    return args
