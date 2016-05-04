#!/usr/bin/python
import argparse,shutil,os
from lxml import etree
from pymicmac import utils_execution

def run(inputFile, outputFolder, num):
    if num % 2:
        raise Exception('num must be an even number!')
    e = etree.parse(inputFile).getroot()
    shutil.rmtree(outputFolder, True)
    os.makedirs(outputFolder)
    pairs = e.findall('Cple')
    numPairs = len(pairs)
    pairsChunk = []
    imagesSetChunk = set([])
    chunkId = 0
    for i in range(numPairs):
        pair = pairs[i].text
        pairsChunk.append(pair)
        (image1,image2) = pair.split()
        imagesSetChunk.add(image1)
        imagesSetChunk.add(image2)
        if (((i+1) % num) == 0) or (i == (numPairs-1)):
            oName = outputFolder + '/' + str(chunkId) + '_' + os.path.basename(inputFile)
            xmlChunkFile = open(oName, 'w')
            listChunkFile = open(oName + '.list', 'w')

            root = etree.Element('SauvegardeNamedRel')
            for pairChunk in pairsChunk:
                child = etree.Element('Cple')
                child.text = pairChunk
                root.append(child)
            xmlChunkFile.write(etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8'))
            xmlChunkFile.close()

            for image in imagesSetChunk:
                listChunkFile.write(image + '\n')
            listChunkFile.close()

            pairsChunk = []
            imagesSetChunk = set([])
            chunkId+=1


def argument_parser():
   # define argument menu
    description = ""
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-i', '--input', default='', help='', type=str, required=True)
    parser.add_argument('-o', '--output', default='', help='', type=str, required=True)
    parser.add_argument('-n', '--num', default='', help='', type=int, required=True)
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.input, a.output, a.num)
    except Exception as e:
        print(e)
