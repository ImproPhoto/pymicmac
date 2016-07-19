#!/usr/bin/python
import os, argparse, glob, os, sys
from lxml import etree
from pymicmac import utils_execution

def run(dataDir, configFile, setEnvironmentFileToSource, remoteExeDir, localOutDir, qsuboptions):

    e = etree.parse(configFile).getroot()
    numComponents = len(e.findall('Component'))

    scriptsParentPath = os.path.dirname(os.path.realpath(__file__))
    executable = scriptsParentPath + '/run_distributed_workflow_sge_job.sh'
    executable_python = scriptsParentPath + '/run_distributed_workflow_sge_job.py'

    configFileAbsPath = os.path.abspath(configFile)
    dataDirAbsPath = os.path.abspath(dataDir)
    localOutDirAbsPath = os.path.abspath(localOutDir)

    for i in range(numComponents):
        print('qsub ' + qsuboptions + ' ' + executable + ' ' + setEnvironmentFileToSource + ' ' + executable_python + ' ' + configFileAbsPath + ' ' + str(i) + ' ' + dataDirAbsPath + ' ' + remoteExeDir + ' ' + localOutDirAbsPath)


def argument_parser():
   # define argument menu
    description = "Creates the jobs to submit to a SGE cluster for a MicMac XML distributed computing workflow. For each executed command there is monitoring of used CPU/MEM/disk."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--dataDir',default='', help='Data directory with the images and the distribution configuration folder (this has to be shared and accessible from the cluster nodes)', type=str, required=True)
    parser.add_argument('-c', '--configFile',default='', help='MicMac XML distributed computing workflow configuration file with the several commands that will be executed in parallel through in SGE cluster. This file must be in the data directory', type=str, required=True)
    parser.add_argument('-s', '--source',default='', help='Set environment file (this file is sourced before the remote execution of any command, the file must be in a shared folder and be accessible from the cluster nodes)', type=str, required=True)
    parser.add_argument('-r', '--remoteExeDir',default='', help='Remote execution directory. Each command will be executed in a cluster node in a folder like <remoteExeDir>/<commandId>', type=str, required=True)
    parser.add_argument('-o', '--localOutDir',default='', help='Local output folder. The execution of each command of the workflow will be done in a remote folder in a SGE node, but the output specified in the configuration XML will be copied to a local folder <localOutDir>/<commandId>', type=str, required=True)
    parser.add_argument('--qsuboptions',default='-l h_rt=00:15:00 -N dpymicmac', help='Options to pass to qsub command. At least must include a -N <name> [default is "-l h_rt=00:15:00 -N dpymicmac"]', type=str, required=False)
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.dataDir, a.configFile, a.source, a.remoteExeDir, a.localOutDir, a.qsuboptions)
    except Exception as e:
        print(e)
