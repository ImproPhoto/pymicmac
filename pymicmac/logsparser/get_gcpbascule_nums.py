 #!/usr/bin/python
import sys, numpy, os, math
from tabulate import tabulate
import xml.etree.ElementTree

gcpsXYZ = {}
cpsXYZ = {}

xmlFile = sys.argv[1]

if not os.path.isfile(xmlFile):
    print('ERROR: ' + xmlFile + ' not found')
    sys.exit(1)

e = xml.etree.ElementTree.parse(xmlFile).getroot()
for p in e.findall('OneAppuisDAF'):
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

tableGCPs = []
tableCPs = []
tableKOs = []

for i in range(2,len(sys.argv)):
    folderName = sys.argv[i]
    if folderName.endswith('/'):
        folderName = folderName[:-1]

    logFileName = folderName + '/GCPBascule.log'

    if os.path.isfile(logFileName):
        lines = open(logFileName,'r').read().split('\n')
        (dsGCPs,usGCPs,vsGCPs,wsGCPs) = ([],[],[],[])
        (dsCPs,usCPs,vsCPs,wsCPs) = ([],[],[],[])

        gcpKOs = []

        for line in lines:
            if line.count('Dist'):
                gcp = line.split()[1]
                fields = line.split('[')[-1].split(']')[0].split(',')
                # u = math.fabs(float(fields[0]))
                # v = math.fabs(float(fields[1]))
                # w = math.fabs(float(fields[2]))
                d = float(line.split('Dist')[-1].split()[0].split('=')[-1])

                if gcp in gcpsXYZ:
                    dsGCPs.append(d)
                    # usGCPs.append(u)
                    # vsGCPs.append(v)
                    # wsGCPs.append(w)
                elif gcp in cpsXYZ:
                    dsCPs.append(d)
                    # usCPs.append(u)
                    # vsCPs.append(v)
                    # wsCPs.append(w)
                else:
                    print('GCP/CP: ' + gcp + ' not found')
                    sys.exit(1)
            elif line.count('NOT OK'):
                gcpKOs.append(line.split(' ')[4])

        if len(gcpKOs):
            tableKOs.append([folderName ,','.join(gcpKOs)])
        else:
            tableKOs.append([folderName ,'-'])

        pattern = "%0.4f"
        if len(dsGCPs):
            tableGCPs.append([folderName, pattern % numpy.min(dsGCPs), pattern % numpy.max(dsGCPs), pattern % numpy.mean(dsGCPs), pattern % numpy.std(dsGCPs), pattern % numpy.median(dsGCPs)])
            #tableGCPs.append([folderName, pattern % numpy.mean(dsGCPs), pattern % numpy.std(dsGCPs), pattern % numpy.mean(usGCPs), pattern % numpy.std(usGCPs), pattern % numpy.mean(vsGCPs), pattern % numpy.std(vsGCPs), pattern % numpy.mean(wsGCPs), pattern % numpy.std(wsGCPs)])
        else:
            tableGCPs.append([folderName, '-', '-', '-', '-', '-'])
            #tableGCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])
        if len(dsCPs):
            tableCPs.append([folderName, pattern % numpy.min(dsCPs), pattern % numpy.max(dsCPs), pattern % numpy.mean(dsCPs), pattern % numpy.std(dsCPs), pattern % numpy.median(dsCPs)])
            #tableCPs.append([folderName, pattern % numpy.mean(dsCPs), pattern % numpy.std(dsCPs), pattern % numpy.mean(usCPs), pattern % numpy.std(usCPs), pattern % numpy.mean(vsCPs), pattern % numpy.std(vsCPs), pattern % numpy.mean(wsCPs), pattern % numpy.std(wsCPs)])
        else:
            tableCPs.append([folderName, '-', '-', '-', '-', '-'])
            #tableCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])
    else:
        tableKOs.append([folderName ,'-'])

        tableGCPs.append([folderName, '-', '-', '-', '-', '-'])
        #tableGCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])
        tableCPs.append([folderName, '-', '-', '-', '-', '-'])
        #tableCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])

print("###########################")
print("GCPBascule Dists statistics")
print("###########################")
print('KOs')
print(tabulate(tableKOs, headers=['#Name', '',]))
print()

header = ['#Name', 'Min', 'Max', 'Mean', 'Std', 'Median']
#header = ['#Name', 'MeanDist', 'StdDist', 'MeanXDist', 'StdXDist', 'MeanYDist', 'StdYDist', 'MeanZDist', 'StdZDist']

print('GCPs')
print(tabulate(tableGCPs, headers=header))
print()

print('CPs')
print(tabulate(tableCPs, headers=header))
print()
