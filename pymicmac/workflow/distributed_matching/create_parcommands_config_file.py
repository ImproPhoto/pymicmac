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


def run(orientationFolder, homolFolder, imagesFormat, numNeighbours, outputFile, outputFolder, num, includeHomol):
    # Check user parameters
    if not os.path.isdir(orientationFolder):
        raise Exception(orientationFolder + ' does not exist')
    if not os.path.isdir(homolFolder):
        raise Exception(homolFolder + ' does not exist')

    if os.path.isfile(outputFile):
        raise Exception(outputFile + ' already exists!')
    if os.path.isdir(outputFolder):
        raise Exception(outputFolder + ' already exists!')
    # create output folder
    os.makedirs(outputFolder)

    mmLocalChanDescFile = 'MicMac-LocalChantierDescripteur.xml'
    requireLocalChanDescFile = ''
    if os.path.isfile(mmLocalChanDescFile):
        requireLocalChanDescFile = mmLocalChanDescFile

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

    print("Bounding box: " + ','.join([str(e) for e in [minX, minY,maxX, maxY]]))
    print("Offset bounding box: " + ','.join([str(e) for e in [0, 0,maxX-minX, maxY-minY]]))

    # Compute the size of the tiles in X and Y
    tileSizeX = (maxX - minX) / nX
    tileSizeY = (maxY - minY) / nY

    # Create a KDTree to query nearest neighbours
    kdtree = spatial.KDTree(camera2DPoints)

    # Check that tiles are small enough with the given images
    numSamplePoints = 100
    distances = []
    for camera2DPoint in camera2DPoints[:numSamplePoints]:
        distances.append(kdtree.query(camera2DPoint, 2)[0][1])
    meanDistance = numpy.mean(distances)
#    if tileSizeX > meanDistance:
#        raise Exception("Increase number of tiles in X. It has to be higher than " + str(int(nX * (tileSizeX/meanDistance))))
#    if tileSizeY > meanDistance:
#        raise Exception("Increase number of tiles in Y. It has to be higher than " + str(int(nY * (tileSizeY/meanDistance))))

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
    oFile = open(outputFile, 'w')
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
            imagesTileSet.update([images[nni] for nni in kdtree.query((tMinX, tMinY), numNeighbours)[1]])
            imagesTileSet.update([images[nni] for nni in kdtree.query((tMinX, tMaxY), numNeighbours)[1]])
            imagesTileSet.update([images[nni] for nni in kdtree.query((tMaxX, tMinY), numNeighbours)[1]])
            imagesTileSet.update([images[nni] for nni in kdtree.query((tMaxX, tMaxY), numNeighbours)[1]])

            if includeHomol:
                imagesTileSetFinal = imagesTileSet.copy()
                # Add to the images for this tile, othe rimages that have tie-points with the current images in the tile
                for image in imagesTileSet:
                     imagesTileSetFinal.update([e.replace('.dat','') for e in os.listdir(homolFolder + '/Pastis' + image)])
                imagesTileSet = imagesTileSetFinal

            if len(imagesTileSet) == 0:
                raise Exception('EMPTY TILE!')

            tileName = 'tile_' + str(i) + '_' + str(j)

            # Dump the list of images for this tile
            tileImageListOutputFileName = outputFolder + '/' + tileName + '.list'
            tileImageListOutputFile = open(tileImageListOutputFileName, 'w')
            tileImageListOutputFile.write('\n'.join(sorted(imagesTileSet)))
            tileImageListOutputFile.close()

            childOutput = etree.SubElement(rootOutput, 'Component')

            childOutputId = etree.SubElement(childOutput, 'id')
            childOutputId.text = tileName + '_Matching'

            childOutputImages = etree.SubElement(childOutput, 'requirelist')
            childOutputImages.text =  outputFolder + '/' + os.path.basename(tileImageListOutputFileName)

            childOutputRequire = etree.SubElement(childOutput, 'require')
            childOutputRequire.text = orientationFolder + " " + requireLocalChanDescFile

            childOutputCommand = etree.SubElement(childOutput, 'command')
            command = 'echo -e "\n" | mm3d Malt Ortho ".*' + imagesFormat + '" ' + os.path.basename(orientationFolder) + ' "BoxTerrain=[' + ','.join([str(e) for e in (tMinX, tMinY,tMaxX, tMaxY)]) + ']"'
            command += '; echo -e "\n" | mm3d Tawny Ortho-MEC-Malt'
            command += '; echo -e "\n" | mm3d Nuage2Ply MEC-Malt/NuageImProf_STD-MALT_Etape_8.xml Attr=Ortho-MEC-Malt/Orthophotomosaic.tif Out=' + tileName + '.ply Offs=[' + str(minX) + ',' + str(minY) + ',0]'
            childOutputCommand.text = command

            childOutputOutput = etree.SubElement(childOutput, 'output')
            childOutputOutput.text = tileName + '.ply'

    oFile.write(etree.tostring(rootOutput, pretty_print=True, encoding='utf-8').decode('utf-8'))
    oFile.close()


def argument_parser():
   # define argument menu
    description = "Distributed solution for matching, i.e. point cloud generation from images and orientation. Splits the matching of a large area in the matching of many tiles. IMPORTANT: only use for images oriented in cartographic reference systems (tiling is done assuming Z is zenith), ideally for aerial images."
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-i', '--inputOrientation',default='', help='Orientation folder. Orientation must be in cartographic reference systems', type=str, required=True)
    parser.add_argument('-t', '--inputHomol',default='', help='Homol folder with the tie-points', type=str, required=True)
    parser.add_argument('-e', '--format',default='', help='Images format (example jpg or tif)', type=str, required=True)

    parser.add_argument('--neighbours',default=6, help='For each tile we consider the images whose XY camera position is in the tile and the K nearest images (default is 6) to each vertex of the tile', type=int, required=False)
    parser.add_argument('-o', '--output', default='', help='pycoeman parallel commands XML configuration file', type=str, required=True)
    parser.add_argument('-f', '--folder', default='', help='Output parallel configuration folder where to store the created files required by the distributed tool', type=str, required=True)
    parser.add_argument('-n', '--num', default='', help='Number of tiles in which the XY extent is divided, specifed as numX,numY', type=str, required=True)
    parser.add_argument('--includeHomol', default=False, help='If enabled, for each tile we also consider the homol images of the images in the tile and of the NN images to the vertices [default is disabled]', action='store_true')

    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.inputOrientation, a.inputHomol, a.format, a.neighbours, a.output, a.folder, a.num, a.includeHomol)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
