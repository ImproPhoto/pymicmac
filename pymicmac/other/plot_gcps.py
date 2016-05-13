 #!/usr/bin/python
import sys, os, math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from lxml import etree

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

ax = fig.add_subplot(1, 1, 1, projection='3d')

(xs,ys,zs) = ([],[],[])
for gcp in gcpsXYZ:
    (x,y,z) = gcpsXYZ[gcp]
    xs.append(x)
    ys.append(y)
    zs.append(z)
    ax.text(x, y, z, gcp, color='blue', fontsize=6)
ax.scatter(xs, ys, zs, marker='o', c='blue')

(xs,ys,zs) = ([],[],[])
for cp in cpsXYZ:
    (x,y,z) = cpsXYZ[cp]
    xs.append(x)
    ys.append(y)
    zs.append(z)
    ax.text(x, y, z, cp, color='red', fontsize=6)
ax.scatter(xs, ys, zs, marker='o', c='red')

ax.set_xlabel('X', fontsize=8, labelpad=-5)
ax.set_ylabel('Y', fontsize=8, labelpad=-5)
ax.set_zlabel('Z', fontsize=8, labelpad=-5)

ax.tick_params(labelsize=6, direction='out', pad=-1)
ax.tick_params(axis='z', labelsize=0, pad=-3)

blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
ax.legend([blue_proxy,red_proxy],['GCPs','CPs'], loc='upper right', bbox_to_anchor=(0.9, 0.9),prop={'size':6})
ax.view_init(elev=-90., azim=0.)

plt.show()
