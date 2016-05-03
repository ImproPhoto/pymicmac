 #!/usr/bin/python
import os, argparse
from pymicmac import utils_execution

def run(name, extension, prec, sizeTile, distMul, multiVG, gcp2DFile, gcp3DFile, mountPoint, onlyPrint):
    rootPath = os.getcwd()

    # Initialize test folder (i.e. create link of images, homol folder and GCP files)
    utils_execution.initPipelineFolder(name, extension, ['Homol', gcp3DFile, gcp2DFile])

    # Change directory to test folder
    os.chdir(name)

    # Run Martini command
    options = '".*' + extension + '"'
    command = 'mm3d Martini ' + options
    utils_execution.executeCommandMonitor('Martini', command, mountPoint, onlyPrint)

    # Run OriRedTieP command
    options = '".*' + extension + '"' + ' Prec2P=' + prec + ' SzTile=' + sizeTile + ' DistPMul=' + distMul + ' MVG=' + multiVG
    command = 'mm3d OriRedTieP ' + options
    utils_execution.executeCommandMonitor('OriRedTieP', command, mountPoint, onlyPrint)

    # From now one we use as Homol folder the one we just created
    os.system('rm Homol')
    os.system('mv HomolTiePRed Homol')

    # Run Tapas command
    options = 'Fraser ".*' + extension + '"' + ' Out=TapasOut'
    command = 'mm3d Tapas ' + options
    utils_execution.executeCommandMonitor('Tapas', command, mountPoint, onlyPrint)

    # Run GCPBascule command
    options = '".*' + extension + '" TapasOut GCPBOut ' + gcp3DFile + ' ' + gcp2DFile
    command = 'mm3d GCPBascule ' + options
    utils_execution.executeCommandMonitor('GCPBascule', command, mountPoint, onlyPrint)

    # Run Campari command
#    options = '".*' + extension + '" GCPBOut CamOut GCP=[' + gcp3DFile + ',0.1,' + gcp2DFile + ',0.5]'
#    command = 'mm3d Campari ' + options
#    utils_execution.executeCommandMonitor('Campari', command, mountPoint, onlyPrint)

    # Run AperiCloud command
#    options = '".*' + extension + '" GCPBOut Out=GCPBOut.ply'
#    command = 'mm3d AperiCloud ' + options
#    utils_execution.executeCommandMonitor('AperiCloud', command, mountPoint, onlyPrint)

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
    parser.add_argument('--prec',default='', help='', type=str, required=True)
    parser.add_argument('--sizeTile',default='', help='', type=str, required=True)
    parser.add_argument('--distMul',default='', help='', type=str, required=True)
    parser.add_argument('--multiVG',default='', help='', type=str, required=True)
    parser.add_argument('--gcp2DFile',default='', help='', type=str, required=True)
    parser.add_argument('--gcp3DFile',default='', help='', type=str, required=True)
    parser.add_argument('--mountPoint',default='', help='', type=str, required=True)
    parser.add_argument('--onlyPrint', default=False, action='store_true')
    return parser

if __name__ == "__main__":
    try:
        prec,sizeTile,distMul,multiVG
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.name, a.extension, a.prec, a.sizeTile, a.distMul, a.multiVG, a.gcp2DFile, a.gcp3DFile, a.mountPoint, a.onlyPrint)
    except Exception as e:
        print(e)
