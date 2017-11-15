#!/usr/bin/python
import argparse
import shutil
import os
from lxml import etree
from pymicmac import utils_execution


def run(inputFile, outputFile, outputFolder, num):
    # Check user parameters
    if not os.path.isfile(inputFile):
        raise Exception(inputFile + ' does not exist')
    if os.path.isfile(outputFile):
        raise Exception(outputFile + ' already exists!')
    outputFileAbsPath = os.path.abspath(outputFile)
    if os.path.isdir(outputFolder):
        raise Exception(outputFolder + ' already exists!')
    if outputFolder[-1] == '/':
        outputFolder = outputFolder[:-1]
    outputFolderAbsPath = os.path.abspath(outputFolder)
    outputFolderName = os.path.basename(outputFolderAbsPath)
    if num % 2:
        raise Exception('num must be an even number!')

    mmLocalChanDescFile = 'MicMac-LocalChantierDescripteur.xml'
    requireLocalChanDescFile = ''
    if os.path.isfile(mmLocalChanDescFile):
        requireLocalChanDescFile = mmLocalChanDescFile

    # Read input XML with valid iamge pairs
    e = etree.parse(inputFile).getroot()
    # Create output folder
    os.makedirs(outputFolderAbsPath)

    # Create output file
    oFile = open(outputFileAbsPath, 'w')
    rootOutput = etree.Element('ParCommands')

    pairs = e.findall('Cple')
    numPairs = len(pairs)
    # Create list of pairs and set of images for a chunk
    pairsChunk = []
    imagesSetChunk = set([])
    chunkId = 0
    errorImagesSet = set([])
    for i in range(numPairs):
        # Add pair and image to current chunk
        pair = pairs[i].text
        pairsChunk.append(pair)
        (image1, image2) = pair.split()

        # image1AbsPath = os.path.abspath(image1)
        # image2AbsPath = os.path.abspath(image2)
        #
        # if not os.path.isfile(image1AbsPath):
        #     errorImagesSet.add(image1AbsPath)
        # if not os.path.isfile(image2AbsPath):
        #     errorImagesSet.add(image2AbsPath)
        #
        # imagesSetChunk.add(image1AbsPath)
        # imagesSetChunk.add(image2AbsPath)

        if not os.path.isfile(image1):
            errorImagesSet.add(image1)
        if not os.path.isfile(image2):
            errorImagesSet.add(image2)
        imagesSetChunk.add(image1)
        imagesSetChunk.add(image2)

        if (((i + 1) % num) == 0) or (i == (numPairs - 1)
                                      ):  # if currernt chunk is full or we just added the lsat pair, we need to store the chunk data
            # Define output files names and absolute paths for this chunk
            chunkXMLFileName = str(chunkId) + '_' + os.path.basename(inputFile)
            chunkImagesListFileName = chunkXMLFileName + '.list'
            chunkXMLFileAbsPath = outputFolderAbsPath + '/' + chunkXMLFileName
            chunkImagesListFileAbsPath = outputFolderAbsPath + '/' + chunkImagesListFileName
            # Open the output files for this chunk
            chunkXMLFile = open(chunkXMLFileAbsPath, 'w')
            chunkImagesListFile = open(chunkImagesListFileAbsPath, 'w')
            # Dump the XML file with image pairs for this chunk
            rootChunk = etree.Element('SauvegardeNamedRel')
            for pairChunk in pairsChunk:
                childChunk = etree.Element('Cple')
                childChunk.text = pairChunk
                rootChunk.append(childChunk)
            chunkXMLFile.write(
                etree.tostring(
                    rootChunk,
                    pretty_print=True,
                    encoding='utf-8').decode('utf-8'))
            chunkXMLFile.close()
            # Dump the .list file with the images in this chunk
            for image in imagesSetChunk:
                chunkImagesListFile.write(image + '\n')
            chunkImagesListFile.close()

            # Add XML component in MicMac XML distributed computing file
            childOutput = etree.Element('Component')

            childOutputId = etree.Element('id')
            childOutputId.text = str(chunkId) + '_Tapioca'
            childOutput.append(childOutputId)

            childOutputImages = etree.Element('requirelist')
            childOutputImages.text = outputFolderName + '/' + chunkImagesListFileName
            childOutput.append(childOutputImages)

            childOutputRequire = etree.Element('require')
            childOutputRequire.text = outputFolderName + '/' + \
                chunkXMLFileName + " " + requireLocalChanDescFile
            childOutput.append(childOutputRequire)

            childOutputCommand = etree.Element('command')
            childOutputCommand.text = 'mm3d Tapioca File ' + chunkXMLFileName + ' -1'
            childOutput.append(childOutputCommand)

            childOutputOutput = etree.Element('output')
            childOutputOutput.text = "Homol"
            childOutput.append(childOutputOutput)

            rootOutput.append(childOutput)
#
            # Empty the chunk
            pairsChunk = []
            imagesSetChunk = set([])
            chunkId += 1

    oFile.write(
        etree.tostring(
            rootOutput,
            pretty_print=True,
            encoding='utf-8').decode('utf-8'))
    oFile.close()

    # for imageAbsPath in errorImagesSet:
    #     print("WARNING: " + os.path.basename(imageAbsPath) + " is not located in " + imageAbsPath + '. If you use relative paths or just the image names, be careful to put the XML in the same folder with the images')

    for image in errorImagesSet:
        print(
            "WARNING: " +
            image +
            " could not be found. The XML with the valid image pairs must be located in the same folder with the images")


def argument_parser():
   # define argument menu
    description = "Splits a valid image pairs file suitable for Tapioca into chunks. For each chunk, it adds a component in a pycomean parallel commands XML configuration file, and it stores in a parallel configuration folder the information of the chunk "
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument(
        '-i',
        '--input',
        default='',
        help='Input XML valid image pair file',
        type=str,
        required=True)
    parser.add_argument(
        '-o',
        '--output',
        default='',
        help='pycoeman parallel commands XML configuration file',
        type=str,
        required=True)
    parser.add_argument(
        '-f',
        '--folder',
        default='',
        help='Output parallel configuration folder where to store the created files. For each chunk there will be a XML file with image pairs and a .list file with a list of files',
        type=str,
        required=True)
    parser.add_argument(
        '-n',
        '--num',
        default='',
        help='Number of image pairs per chunk (must be even number)',
        type=int,
        required=True)
    return parser


def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.input, a.output, a.folder, a.num)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
