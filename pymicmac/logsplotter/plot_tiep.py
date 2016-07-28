#!/usr/bin/env python
import sys, os, math, argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pymicmac import utils_execution

def run(inputArgument, maxX, maxY):
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

def argument_parser():
   # define argument menu
    description = "Plots the tie-points from a single tie-points file of from the files of an image subfolder Homol folder"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input',default='', help='Input argument. Can be a single tie-points file or a subfolder in Homol folder (tie-points files must be in ASCII format, use ExpTxt=1 when running Tapioca)', type=str, required=True)
    parser.add_argument('--maxx',default='', help='Maximum X value', type=int, required=True)
    parser.add_argument('--maxy',default='', help='Maximum Y value', type=int, required=True)
    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.input, a.maxx, a.maxy)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
