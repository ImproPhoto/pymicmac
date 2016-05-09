 #!/usr/bin/python
import sys, os, math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from lxml import etree
from tabulate import tabulate

gcpsXYZ = {}
cpsXYZ = {}

xmlFile = sys.argv[1]

if not os.path.isfile(xmlFile):
    print('ERROR: ' + xmlFile + ' not found')
    sys.exit(1)

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

fig = plt.figure(figsize=(27,15))
fig.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.005, hspace=0.005)

gcpsUVW = {}
cpsUVW = {}

numTests = len(sys.argv) - 2

nY = int(math.ceil(math.sqrt(numTests)))
nX = int(math.ceil(numTests / nY))

numAxis = int(math.ceil(math.sqrt(numTests)))

for i in range(numTests):
    folderName = sys.argv[i+2]
    if folderName.endswith('/'):
        folderName = folderName[:-1]
    logFileName = folderName + '/GCPBascule.log'

    if os.path.isfile(logFileName):
        lines = open(logFileName,'r').read().split('\n')
        dists = []

        gcpsUVW[folderName] = {}
        cpsUVW[folderName] = {}

        for line in lines:
            if line.count('Dist'):
                gcp = line.split()[1]
                fields = line.split('[')[-1].split(']')[0].split(',')
                u = float(fields[0])
                v = float(fields[1])
                w = float(fields[2])
                d = float(line.split('Dist')[-1].split()[0].split('=')[-1])

                if gcp in cpsXYZ:
                    cpsUVW[folderName][gcp] = (u, v, w, d)
                elif gcp in gcpsXYZ:
                    gcpsUVW[folderName][gcp] = (u, v, w, d)
                else:
                    print('GCP/CP: ' + gcp + ' not found')
                    sys.exit(1)

        ax = fig.add_subplot(nX, nY, i+1, projection='3d')

        (xs,ys,zs,us,vs,ws) = ([],[],[],[],[],[])
        for gcp in gcpsUVW[folderName]:
            (x,y,z) = gcpsXYZ[gcp]
            (u,u,w,_) = gcpsUVW[folderName][gcp]
            xs.append(x)
            ys.append(y)
            zs.append(z)
            us.append(u)
            vs.append(v)
            ws.append(w)
            # print(x, y, z, u, v, w)
            ax.text(x, y, z, gcp, color='blue', fontsize=6)
        ax.scatter(xs, ys, zs, marker='o', c='blue')
        ax.quiver(xs, ys, zs, us, vs, ws, length=1.0, pivot="tail", color='blue')

        (xs,ys,zs,us,vs,ws) = ([],[],[],[],[],[])
        for cp in cpsUVW[folderName]:
            (x,y,z) = cpsXYZ[cp]
            (u,u,w,_) = cpsUVW[folderName][cp]
            xs.append(x)
            ys.append(y)
            zs.append(z)
            us.append(u)
            vs.append(v)
            ws.append(w)
            # print(x, y, z, u, v, w)
            ax.text(x, y, z, cp, color='red', fontsize=6)
        ax.scatter(xs, ys, zs, marker='o', c='red')
        ax.quiver(xs, ys, zs, us, vs, ws, length=1.0, pivot="tail", color='red')


        ax.set_xlabel('X', fontsize=8, labelpad=-5)
        ax.set_ylabel('Y', fontsize=8, labelpad=-5)
        ax.set_zlabel('Z', fontsize=8, labelpad=-5)
        ax.set_title(folderName, fontsize=8)
        ax.tick_params(labelsize=6, direction='out', pad=-1)
        ax.tick_params(axis='z', labelsize=0, pad=-3)

        blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
        red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
        ax.legend([blue_proxy,red_proxy],['GCPs','CPs'], loc='upper right', bbox_to_anchor=(0.9, 0.9),prop={'size':6})
        ax.view_init(elev=-90., azim=0.)

        # ax.set_zlim(1,6)

table = []
for gcp in sorted(gcpsXYZ):
    row = [gcp,]
    for i in range(numTests):
        folderName = sys.argv[i+2]
        if folderName in gcpsUVW and gcp in gcpsUVW[folderName]:
            row.append(gcpsUVW[folderName][gcp][-1])
        else:
            row.append('-')
    table.append(row)

print("##########################")
print("GCPBascule Dist per GCP/CP")
print("##########################")

header = ['GCP',] + sys.argv[2:]
print(tabulate(table, headers=header))
print()

table = []
for cp in sorted(cpsXYZ):
    row = [cp,]
    for i in range(numTests):
        folderName = sys.argv[i+2]
        if folderName in cpsUVW and cp in cpsUVW[folderName]:
            row.append(cpsUVW[folderName][cp][-1])
        else:
            row.append('-')
    table.append(row)

header = ['CP',] + sys.argv[2:]
print(tabulate(table, headers=header))
print()


plt.show()
