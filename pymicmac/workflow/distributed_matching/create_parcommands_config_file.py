#!/usr/bin/python
import argparse, os, glob
import numpy
from pymicmac import utils_execution
from lxml import etree
from scipy import spatial

def getTileIndex(pX, pY, minX, minY, maxX, maxY, nX, nY):
    xpos = int((pX - minX) * nX / (maxX - minX))
    ypos = int((pY - minY) * nY / (maxY - minY))
    if xpos == nX: # If it is in the edge of the box (in the maximum side) we need to put in the last tile
        xpos -= 1
    if ypos == nY:
        ypos -= 1
    return (xpos, ypos)


def run(orientationFolder, homolFolder, matchingXML, matchingScript, numNeighbours, outputFile, outputFolder, num):
    # Check user parameters
    orientationFolderAbsPath = os.path.abspath(orientationFolder)
    homolFolderAbsPath =  os.path.abspath(homolFolder)
    matchingXMLAbsPath = os.path.abspath(matchingXML)
    matchingScriptAbsPath = os.path.abspath(matchingScript)
    if not os.path.isdir(orientationFolderAbsPath):
        raise Exception(orientationFolderAbsPath + ' does not exist')
    if not os.path.isdir(homolFolderAbsPath):
        raise Exception(homolFolderAbsPath + ' does not exist')
    if not os.path.isfile(matchingXMLAbsPath):
        raise Exception(matchingXMLAbsPath + ' does not exist')
    if not os.path.isfile(matchingScriptAbsPath):
        raise Exception(matchingScriptAbsPath + ' does not exist')

    outputFileAbsPath = os.path.abspath(outputFile)
    outputFolderAbsPath = os.path.abspath(outputFolder)
    if os.path.isfile(outputFile):
        raise Exception(outputFile + ' already exists!')
    if os.path.isdir(outputFolder):
        raise Exception(outputFolder + ' already exists!')
    outputFolderName = os.path.basename(outputFolderAbsPath)

    # create output folder
    os.makedirs(outputFolderAbsPath)
    # Parse number of tiles in X and Y
    nX,nY = [int(e) for e in num.split(',')]

    # Initialize the empty lists of images and 2D points with the x,y positions of the cameras
    images = []
    camera2DPoints = []

    # For each image we get the x,y position of the camera and we add the image and th epoint in the lists
    orientationFiles = glob.glob(orientationFolder + '/Orientation*')
    for orientationFile in orientationFiles:
        images.append(os.path.basename(orientationFile).replace("Orientation-","").replace(".xml",""))
        e = etree.parse(orientationFile).getroot()
        (x,y,_) = [float(c) for c in e.xpath("//Externe")[0].find('Centre').text.split()]
        camera2DPoints.append((x,y))

    if numNeighbours >= len(images):
        raise Exception("numNeighbours >= len(images)")

    # Compute the bounding box of all the camera2DPoints
    minX, minY = numpy.min(camera2DPoints, axis=0)
    maxX, maxY = numpy.max(camera2DPoints, axis=0)
    # Compute the size of the tiles in X and Y
    tileSizeX = (maxX - minX) / nX
    tileSizeY = (maxY - minY) / nY


    # Create a KDTree to query nearest neighbours
    kdtree = spatial.KDTree(camera2DPoints)

    # For each tile first we get a list of images whose camera XY position lays within the tile
    # note: there may be empty tiles
    tilesImages = {}
    for i,camera2DPoint in enumerate(camera2DPoints):
        pX,pY = camera2DPoint
        tileIndex = getTileIndex(pX, pY, minX, minY, maxX, maxY, nX, nY)
        if tileIndex not in tilesImages:
            tilesImages[tileIndex] = [images[i],]
        else:
            tilesImages[tileIndex].append(images[i])

    # Create output file
    oFile = open(outputFileAbsPath, 'w')
    rootOutput = etree.Element('ParCommands')

    # For each tile we extend the tilesImages list with the nearest neighbours
    for i in range(nX):
        for j in range(nY):
            k = (i,j)
            (tMinX, tMinY) = (minX + (i * tileSizeX), minY + (j * tileSizeY))
            (tMaxX, tMaxY) = (tMinX + tileSizeX, tMinY + tileSizeY)
            tCenterX = tMinX + ((tMaxX - tMinX) / 2.)
            tCenterY = tMinY + ((tMaxY - tMinY) / 2.)
            if k in tilesImages:
                imagesTile = tilesImages[k]
            else:
                imagesTile = []
            imagesTileSet = set(imagesTile)

            imagesTileSet.update([images[nni] for nni in kdtree.query((tCenterX, tCenterY), numNeighbours)[1]])

            imagesTileSetFinal = imagesTileSet.copy()
            # Add to the images for this tile, othe rimages that have tie-points with the current images in the tile
            for image in imagesTileSet:
                 imagesTileSetFinal.update([e.replace('.dat','') for e in os.listdir(homolFolderAbsPath + '/Pastis' + image)])

            if len(imagesTileSetFinal) == 0:
                raise Exception('EMPTY TILE!')

            tileName = 'tile_' + str(i) + '_' + str(j)

            # Dump the list of images for this tile
            tileImageListOutputFileName = outputFolderAbsPath + '/' + tileName + '.list'
            tileImageListOutputFile = open(tileImageListOutputFileName, 'w')
            tileImageListOutputFile.write('\n'.join(sorted(imagesTileSetFinal)))
            tileImageListOutputFile.close()

            # Create the MicMac configuration for this tile
            tileMicMacConfigXMLFileName = outputFolderAbsPath + '/' + tileName + '_' + os.path.basename(matchingXMLAbsPath)
            tileMicMacConfigXMLFile = open(tileMicMacConfigXMLFileName, 'w')
            e = etree.parse(matchingXMLAbsPath).getroot()

            if i == 0 and j == 0:
                orientationFolderFromMatchingXML = e.xpath('//CalcName')[0].text.strip().split('/')[0]
                if os.path.basename(orientationFolderAbsPath) != orientationFolderFromMatchingXML:
                    raise Exception('The orientation folder in ' + matchingXMLAbsPath + ' is ' + orientationFolderFromMatchingXML + '. Expected is ' + os.path.basename(orientationFolderAbsPath))

            s = e.find('Section_Terrain')
            p = s.find('Planimetrie')
            if p != None:
                s.remove(p)
            p = etree.SubElement(s, 'Planimetrie')
            b = etree.SubElement(p, 'BoxTerrain')
            b.text = ' '.join([str(c) for c in (tMinX, tMinY, tMaxX, tMaxY)])

            tileMicMacConfigXMLFile.write(etree.tostring(e, pretty_print=True, encoding='utf-8').decode('utf-8'))
            tileMicMacConfigXMLFile.close()

            # Create the matching Script
            tileMatchingScriptOutputFileName = outputFolderAbsPath + '/' + tileName + '_' + os.path.basename(matchingScriptAbsPath)
            tileMatchingScriptOutputFile = open(tileMatchingScriptOutputFileName, 'w')
            tileMatchingScriptOutputFile.write(open(matchingScriptAbsPath, 'r').read().replace(os.path.basename(matchingXMLAbsPath),os.path.basename(tileMicMacConfigXMLFileName)))
            tileMatchingScriptOutputFile.close()

            childOutput = etree.SubElement(rootOutput, 'Component')

            childOutputId = etree.SubElement(childOutput, 'id')
            childOutputId.text = tileName + '_Matching'

            childOutputImages = etree.SubElement(childOutput, 'requirelist')
            childOutputImages.text =  outputFolderName + '/' + os.path.basename(tileImageListOutputFileName)

            childOutputRequire = etree.SubElement(childOutput, 'require')
            childOutputRequire.text = outputFolderName + '/' + os.path.basename(tileMicMacConfigXMLFileName) + " " + \
                                      outputFolderName + '/' + os.path.basename(tileMatchingScriptOutputFileName) + " " + \
                                      orientationFolder

            childOutputCommand = etree.SubElement(childOutput, 'command')
            childOutputCommand.text = 'chmod u+x ' + os.path.basename(tileMatchingScriptOutputFileName) + '; ./' + os.path.basename(tileMatchingScriptOutputFileName)

            childOutputOutput = etree.SubElement(childOutput, 'output')
            childOutputOutput.text = e.xpath('//TmpResult')[0].text.strip()

    oFile.write(etree.tostring(rootOutput, pretty_print=True, encoding='utf-8').decode('utf-8'))
    oFile.close()


def argument_parser():
   # define argument menu
    description = "Distributed solution for matching, i.e. point cloud generation from images and orientation. Splits the matching of a large area in the matching of many tiles. IMPORTANT: only use for images oriented in cartographic reference systems (tiling is done assuming Z is zenith), ideally for aerial images."
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-i', '--inputOrientation',default='', help='Orientation folder. Orientation must be in cartographic reference systems', type=str, required=True)
    parser.add_argument('-t', '--inputHomol',default='', help='Homol folder with the tie-points', type=str, required=True)
    parser.add_argument('-c', '--matchingXML',default='', help='XML configuration file for MICMAC matching tool within MicMac suite. This will be used for the matching of each tile, but with the addition of a BoxTerrain option', type=str, required=True)
    parser.add_argument('-s', '--matchingScript',default='', help='Script to run for each tile. One of the commands executed must be MICMAC and it must use the XML specifed with <matchingXML> (this will be replaced accordingly for each tile)', type=str, required=True)

    parser.add_argument('--neighbours',default=9, help='For each tile we consider the nearest images', type=int, required=False)
    parser.add_argument('-o', '--output', default='', help='pycoeman parallel commands XML configuration file', type=str, required=True)
    parser.add_argument('-f', '--folder', default='', help='Output parallel configuration folder where to store the created files required by the distributed tool', type=str, required=True)
    parser.add_argument('-n', '--num', default='', help='Number of tiles in which the XY extent is divided, specifed as numX,numY', type=str, required=True)
    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.inputOrientation, a.inputHomol, a.matchingXML, a.matchingScript, a.neighbours, a.output, a.folder, a.num)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
