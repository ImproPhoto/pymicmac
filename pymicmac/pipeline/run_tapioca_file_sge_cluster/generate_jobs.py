import glob, os, sys

tapiocaMultiFolder = os.path.abspath(sys.argv[1])
setEnvironmentFileToSource = os.path.abspath(sys.argv[2])
sharedWorkDir = os.path.abspath(sys.argv[3])
localWorkDir = os.path.abspath(sys.argv[4])

executable = os.path.abspath('run_tapioca_job.sh')
executable_python = os.path.abspath('run_tapioca_job.py')

for tapiocaXMLFile in glob.glob(tapiocaMultiFolder + '/*xml'):
    print('qsub -l h_rt=00:15:00 -N tapioca ' + executable + ' ' + setEnvironmentFileToSource + ' ' + executable_python + ' ' + tapiocaXMLFile + ' ' + sharedWorkDir + ' ' + localWorkDir)
