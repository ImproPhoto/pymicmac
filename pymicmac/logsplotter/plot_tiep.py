#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys, os, math

inputArgument = sys.argv[1]
maxX = int(sys.argv[2])
maxY = int(sys.argv[3])

if os.path.isdir(inputArgument):
    inputFiles = os.listdir(inputArgument)
    num = len(inputFiles)
    numCols = int(math.ceil(math.sqrt(num)))
    numRows = int(2 * numCols)

    plt.figure(figsize=(18,10))

    gs = gridspec.GridSpec(numRows,numCols)
    gs.update(hspace=0.3)

    for i in range(num):

        lines = open(inputArgument + '/' + inputFiles[i], 'r').read().split('\n')

        x1 = []
        y1 = []
        x2 = []
        y2 = []

        for line in lines:
            fields = line.split()
            if len(fields) == 4:
                x1.append(float(fields[0]))
                y1.append(float(fields[1]))
                x2.append(float(fields[2]))
                y2.append(float(fields[3]))

        ax1 = plt.subplot(gs[int(2 * int(i / numCols)), i % numCols])
        ax2 = plt.subplot(gs[int(1 + (2 * int(i / numCols))), i % numCols])

        vis = False

        ax1.get_xaxis().set_visible(vis)
        ax1.get_yaxis().set_visible(vis)
        ax2.get_xaxis().set_visible(vis)
        ax2.get_yaxis().set_visible(vis)

        ax1.set_xlim([0,maxX])
        ax1.set_ylim([0,maxY])
        ax2.set_xlim([0,maxX])
        ax2.set_ylim([0,maxY])

        ax1.plot(x1, y1, 'b.')
        ax1.set_title(inputArgument + '/' + inputFiles[i], fontsize=6)
        ax2.plot(x2, y2, 'r.')
        #ax2.set_title(inputFiles[i], fontsize=6)
else:
    lines = open(inputArgument, 'r').read().split('\n')

    x1 = []
    y1 = []
    x2 = []
    y2 = []

    for line in lines:
        fields = line.split()
        if len(fields) == 4:
            x1.append(float(fields[0]))
            y1.append(float(fields[1]))
            x2.append(float(fields[2]))
            y2.append(float(fields[3]))

    plt.subplot(2, 1, 1)
    plt.plot(x1, y1, 'b.')

    plt.title(inputArgument)

    plt.subplot(2, 1, 2)
    plt.plot(x2, y2, 'r.')

    plt.set_xlim([0,maxX])
    plt.set_ylim([0,maxY])

plt.show()
