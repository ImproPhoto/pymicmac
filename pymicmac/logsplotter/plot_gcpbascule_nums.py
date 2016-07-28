 #!/usr/bin/python
import os, math,argparse
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from lxml import etree
from tabulate import tabulate
from pymicmac import utils_execution

def run(xmlFile, foldersNames):

    (gcpsXYZ, cpsXYZ) = utils_execution.readGCPXMLFile(xmlFile)

    fig = plt.figure(figsize=(27,15))
    fig.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0.005, hspace=0.005)

    gcpsUVW = {}
    cpsUVW = {}

    foldersNames = foldersNames.split(',')
    numFolders = len(foldersNames)

    nY = int(math.ceil(math.sqrt(numFolders)))
    nX = int(math.ceil(numFolders / nY))

    numAxis = int(math.ceil(math.sqrt(numFolders)))

    for i in range(numFolders):
        if foldersNames[i].endswith('/'):
            foldersNames[i] = foldersNames[i][:-1]

    for i in range(numFolders):
        folderName = foldersNames[i]
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
                        raise Exception('GCP/CP: ' + gcp + ' not found')

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
            # ax.tick_params(axis='z', labelsize=0, pad=-3)

            blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
            red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
            ax.legend([blue_proxy,red_proxy],['GCPs','CPs'], loc='upper right', bbox_to_anchor=(0.9, 0.9),prop={'size':6})
            ax.view_init(elev=-90., azim=0.)

            # ax.set_zlim(1,6)


    print("##########################")
    print("GCPBascule Dist per GCP/CP")
    print("##########################")

    table = []
    for gcp in sorted(gcpsXYZ):
        row = [gcp,]
        for i in range(numFolders):
            folderName = foldersNames[i]
            if folderName in gcpsUVW and gcp in gcpsUVW[folderName]:
                row.append(gcpsUVW[folderName][gcp][-1])
            else:
                row.append('-')
        table.append(row)

    header = ['GCP',] + foldersNames
    print(tabulate(table, headers=header))
    print()

    table = []
    for cp in sorted(cpsXYZ):
        row = [cp,]
        for i in range(numFolders):
            folderName = foldersNames[i]
            if folderName in cpsUVW and cp in cpsUVW[folderName]:
                row.append(cpsUVW[folderName][cp][-1])
            else:
                row.append('-')
        table.append(row)

    header = ['CP',] + foldersNames
    print(tabulate(table, headers=header))
    print()

    plt.show()

def argument_parser():
   # define argument menu
    description = "Plots a 3D quiver of GCPBascule runs in one or more execution folders"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-x', '--xml',default='', help='XML file with the 3D position of the GCPs (and possible CPs)', type=str, required=True)
    parser.add_argument('-f', '--folders',default='', help='Comma-separated list of execution folders where to look for the GCPBascule.log files', type=str, required=True)
    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.xml, a.folders)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
