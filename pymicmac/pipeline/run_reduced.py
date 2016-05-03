 #!/usr/bin/python
import os
from pymicmac import utils_execution

def run(name, extension, nX, nY, adaptive, gain_mode, threshold, ordering, gcp2DFile, gcp3DFile, noodlesNumProc, mountPoint, onlyPrint):
    rootPath = os.getcwd()

    # Initialize pipeline folder (i.e. create link of images, homol folder and GCP files)
    utils_execution.initPipelineFolder(name, extension, ['Homol', gcp3DFile, gcp2DFile])

    # Change directory to pipeline folder
    os.chdir(name)

    # Run PreRedTieP command
    options = '".*' + extension + '" Quick=1'
    command = 'mm3d TestLib NO_AllOri2Im ' + options
    utils_execution.executeCommandMonitor('Pre_RedTieP', command, mountPoint, onlyPrint)

    # Run RedTieP command
    if ordering == "0":
        order_options = " SortByNum=0 Desc=0 ExpSubCom=0"
    elif ordering == "1":
        order_options = " SortByNum=0 Desc=1 ExpSubCom=0"
    elif ordering == "2":
        order_options = " SortByNum=1 Desc=0 ExpSubCom=0"
    elif ordering == "3":
        order_options = " SortByNum=1 Desc=1 ExpSubCom=0"
    elif ordering == "4":
        order_options = " SortByNum=0 Desc=0 ExpSubCom=1"

    options = '".*' + extension + '"' + ' NumPointsX=' + nX + ' NumPointsY=' + nY + ' Adaptive=' + adaptive + ' GainMode=' + gain_mode + ' ThresholdAccMult=' + threshold + order_options
    command = 'mm3d RedTieP ' + options
    utils_execution.executeCommandMonitor('RedTieP', command, mountPoint, onlyPrint)

    if ordering == "4":
         noodlesExePath = os.path.abspath(os.path.join(os.path.realpath(__file__),'../../noodles/noodles_exe_parallel.py'))
         command = 'python ' + noodlesExePath + ' -j ' + str(noodlesNumProc) + ' subcommands.json RedTieP_logs'
         utils_execution.executeCommandMonitor('Noodles', command, mountPoint, onlyPrint)

    # From now one we use as Homol folder the one we just created
    os.system('rm Homol')
    os.system('mv Homol-Red Homol')

    # Run Tapas command
    options = 'Fraser ".*' + extension + '"' + ' Out=TapasOut'
    command = 'mm3d Tapas ' + options
    utils_execution.executeCommandMonitor('Tapas', command, mountPoint, onlyPrint)

    # Run GCPBascule command
    options = '".*' + extension + '" TapasOut GCPBOut ' + gcp3DFile + ' ' + gcp2DFile
    command = 'mm3d GCPBascule ' + options
    utils_execution.executeCommandMonitor('GCPBascule', command, mountPoint, onlyPrint)

    # Run Campari command
#    options = '".*' + extension + '" GCPBOut CamOut GCP=[gcp_List3D.xml,0.1,coord_List2D.xml,0.5]'
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
    parser.add_argument('--nX',default='', help='', type=str, required=True)
    parser.add_argument('--nY',default='', help='', type=str, required=True)
    parser.add_argument('--adaptive',default='', help='', type=str, required=True)
    parser.add_argument('--gain_mode',default='', help='', type=str, required=True)
    parser.add_argument('--threshold',default='', help='', type=str, required=True)
    parser.add_argument('--ordering',default='', help='', type=str, required=True)
    parser.add_argument('--gcp2DFile',default='', help='', type=str, required=True)
    parser.add_argument('--gcp3DFile',default='', help='', type=str, required=True)
    parser.add_argument('--noodlesNumProc',default='', help='', type=str, required=True)
    parser.add_argument('--mountPoint',default='', help='', type=str, required=True)
    parser.add_argument('--onlyPrint', default=False, action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.name, a.extension, a.nX, a.nY, a.adaptive, a.gain_mode, a.threshold, a.ordering, a.gcp2DFile, a.gcp3DFile, a.noodlesNumProc, a.mountPoint, a.onlyPrint)
    except Exception as e:
        print e
