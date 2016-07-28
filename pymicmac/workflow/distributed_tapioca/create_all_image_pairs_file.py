#!/usr/bin/python
import argparse,os
from pymicmac import utils_execution

def run(inputFolder, imageFormat, outputFile):
    # Check user parameters
    if not os.path.isdir(inputFolder):
        raise Exception(inputFolder + " does not exist! (or is not a folder)")
    # Create lists of images that have the correct format
    images = sorted(os.listdir(inputFolder))
    imagesFormat = []
    for image in images:
        if image.endswith(imageFormat):
            imagesFormat.append(image)

    if os.path.isfile(outputFile):
        raise Exception(outputFile + ' already exists!')
    ofile = open(outputFile, 'w')
    ofile.write('<?xml version="1.0" ?>\n')
    ofile.write('<SauvegardeNamedRel>\n')
    for i in range(len(imagesFormat)):
        for j in  range(len(imagesFormat)):
            if i < j:
                ofile.write('     <Cple>' + imagesFormat[i] + ' ' + imagesFormat[j] + '</Cple>\n')
                ofile.write('     <Cple>' + imagesFormat[j] + ' ' + imagesFormat[i] + '</Cple>\n')
    ofile.write('</SauvegardeNamedRel>\n')
    ofile.close()

def argument_parser():
   # define argument menu
    description = "Creates a valid image pairs file suitable for Tapioca (to run with option File). Every possible image pair is added"
    parser = argparse.ArgumentParser(description=description)
    # fill argument groups
    parser.add_argument('-i', '--input', default='', help='Input folder with the images', type=str, required=True)
    parser.add_argument('-f', '--format', default='', help='File format of the images (only files with this format are considered for the pairs)', type=str, required=True)
    parser.add_argument('-o', '--output', default='', help='Output valid image pairs file', type=str, required=True)
    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.input, a.format, a.output)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
