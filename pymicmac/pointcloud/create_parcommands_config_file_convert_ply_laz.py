#!/usr/bin/python
import argparse, os, glob, json
import numpy
from pymicmac import utils_execution
from lxml import etree

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def run(inputFolder, outputFile, outputFormat, outputFolder, num):
    # Check user parameters
    if not os.path.isdir(inputFolder):
        raise Exception(inputFolder + ' does not exist')
    # Check output file and folder
    if os.path.isfile(outputFile):
        raise Exception(outputFile + ' already exists!')
    if os.path.isdir(outputFolder):
        raise Exception(outputFolder + ' already exists!')
    # create output folder
    os.makedirs(outputFolder)
    # Check format
    if outputFormat not in ('las','laz'):
        raise Exception('output format must be las or laz')

    inputFiles = glob.glob(inputFolder + '/*ply')

    # Create output file
    oFile = open(outputFile, 'w')
    globalXMLRootElement = etree.Element('ParCommands')

    # For each tile we extend the tilesImages list with the nearest neighbours
    chunkId = 0
    for chunk in chunks(inputFiles, num):
        chunkXMLFileName =  str(chunkId) + '.xml'
        chunkXMLRelPath = outputFolder + '/' + chunkXMLFileName
        chunkXMLFile = open(chunkXMLRelPath, 'w')
        chunkXMLRootElement = etree.Element('ParCommands')

        chunkFiles = []
        chunkOutputFiles = []

        for inputFile in chunk:
            inputFileName = os.path.basename(inputFile)
            convertedFileName = inputFileName.replace('ply', outputFormat)

            pdalConfig = {
              "pipeline":[
                {
                  "type":"readers.ply",
                  "filename":inputFileName
                },
                {
                  "type":"writers.las",
                  "filename":convertedFileName
                }
              ]
            }

            pdalConfigOutputFileName = inputFileName + '.json'
            pdalConfigOutputFileRelPath = outputFolder + '/' + pdalConfigOutputFileName
            taskName = inputFileName + '_Conversion'

            with open(pdalConfigOutputFileRelPath, 'w') as outfile:
                json.dump(pdalConfig, outfile)

            childOutput = etree.SubElement(chunkXMLRootElement, 'Component')

            childOutputId = etree.SubElement(childOutput, 'id')
            childOutputId.text = taskName

            childOutputRequire = etree.SubElement(childOutput, 'require')
            childOutputRequire.text = pdalConfigOutputFileName + ' ' + inputFileName

            childOutputCommand = etree.SubElement(childOutput, 'command')
            childOutputCommand.text = 'pdal pipeline ' + pdalConfigOutputFileName

            chunkFiles.append(pdalConfigOutputFileRelPath)
            chunkFiles.append(inputFile)

            chunkOutputFiles.append('outputData/' + taskName + '/' + convertedFileName)

        chunkXMLFile.write(etree.tostring(chunkXMLRootElement, pretty_print=True, encoding='utf-8').decode('utf-8'))
        chunkXMLFile.close()

        childOutput = etree.SubElement(globalXMLRootElement, 'Component')

        childOutputId = etree.SubElement(childOutput, 'id')
        childOutputId.text = str(chunkId) + '_Conversion'

        childOutputRequire = etree.SubElement(childOutput, 'require')
        childOutputRequire.text = chunkXMLRelPath + ' ' + ' '.join(chunkFiles)

        childOutputCommand = etree.SubElement(childOutput, 'command')
        childOutputCommand.text = ' coeman-par-local -d . -c ' + chunkXMLFileName + ' -e outputData -n ' + str(num)

        childOutputOutput = etree.SubElement(childOutput, 'output')
        childOutputOutput.text = ' '.join(chunkOutputFiles)

        chunkId += 1

    oFile.write(etree.tostring(globalXMLRootElement, pretty_print=True, encoding='utf-8').decode('utf-8'))
    oFile.close()


def argument_parser():
   # define argument menu
    description = "Creates a 2-level pycoeman XML parallel commands configuration file to convert a bunch of ply files into laz/laz using PDAL. The second level is executed with coeman-par-local."
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-i', '--input',default='', help='Input folder with ply files', type=str, required=True)
    parser.add_argument('-o', '--output', default='', help='pycoeman parallel commands XML configuration file', type=str, required=True)
    parser.add_argument('-f', '--format',default='', help='Output format (las/laz)', type=str, required=True)
    parser.add_argument('-x', '--folder', default='', help='Output parallel configuration folder where to store the created files required by the distributed tool', type=str, required=True)
    parser.add_argument('-n', '--num',default='8', help='Parallelization at level 2 (default is 8)', type=int, required=True)
    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.input, a.output, a.format, a.folder, a.num)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
