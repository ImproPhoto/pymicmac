#!/bin/bash
# $1 is the setenv file to be source'd
# $2 is the python script path to execute the SGE job remotely
# $3 is the XML configuration file
# $4 is the index of the command to be executed
# $5 is the data directory in the shared file system (that contains the images)
# $6 is the execution dir in the nodes
# $7 is the output folder in the shared file system

echo "Set environment file: " $1
echo "SGE python script for remote execution: " $2
echo "XML configuration file: " $3
echo "Command index:" $4
echo "Data directory:" $5
echo "Remote execution directory:" $6
echo "Output directory:" $7

source $1
python $2 $3 $4 $5 $6 $7
