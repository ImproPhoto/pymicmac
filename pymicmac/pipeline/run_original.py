 #!/usr/bin/python
import os, argparse
from pymicmac import utils_execution

def run(name, extension, ppfree, affineFree, drMax, gcp2DFile, gcp3DFile, mountPoint, onlyPrint=False):
    rootPath = os.getcwd()

    # Initialize pipeline folder (i.e. create link of images, homol folder and GCP files)
    utils_execution.initPipelineFolder(name, extension, ['Homol', gcp2DFile, gcp3DFile])

    # Change directory to pipeline folder
    os.chdir(name)

    # Run Tapas command
    options = 'Fraser ".*' + extension + '" Out=TapasOut'
    command = 'mm3d Tapas ' + options
    utils_execution.executeCommandMonitor('Tapas', command, mountPoint, onlyPrint)

    # Run GCPBascule command
    options = '".*' + extension + '" TapasOut GCPBOut ' + gcp3DFile + ' ' + gcp2DFile
    command = 'mm3d GCPBascule ' + options
    utils_execution.executeCommandMonitor('GCPBascule', command, mountPoint, onlyPrint)

    # Run Campari command
    # options = '".*' + extension + '" GCPBOut CamOut GCP=[' + gcp3DFile + ',0.1,' + gcp2DFile + ',0.5] PPFree=' + ppfree + ' AffineFree=' + affineFree + ' DRMax=' + drMax
    # command = 'mm3d Campari ' + options
    # utils_execution.executeCommandMonitor('Campari', command, mountPoint, onlyPrint)

    # Run MMTestOrient command
    # options = 'IMG_1032.JPG IMG_1033.JPG GCPBOut '
    # command = 'mm3d MMTestOrient ' + options
    # utils_execution.executeCommandMonitor('MMTestOrient', command, mountPoint, onlyPrint)

    # Change directory to root folder
    os.chdir(rootPath)


def argument_parser():
   # define argument menu
    description = ""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--name',default='', help='', type=str, required=True)
    parser.add_argument('--extension',default='', help='', type=str, required=True)
    parser.add_argument('--ppfree',default='', help='', type=str, required=True)
    parser.add_argument('--affineFree',default='', help='', type=str, required=True)
    parser.add_argument('--drMax',default='', help='', type=str, required=True)
    parser.add_argument('--gcp2DFile',default='', help='', type=str, required=True)
    parser.add_argument('--gcp3DFile',default='', help='', type=str, required=True)
    parser.add_argument('--mountPoint',default='', help='', type=str, required=True)
    parser.add_argument('--onlyPrint', default=False, action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.name, a.extension, a.ppfree, a.affineFree, a.drMax, a.gcp2DFile, a.gcp3DFile, a.mountPoint, a.onlyPrint)
    except Exception as e:
        print(e)
