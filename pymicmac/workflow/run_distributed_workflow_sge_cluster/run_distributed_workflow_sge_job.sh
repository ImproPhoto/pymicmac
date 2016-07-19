#!/bin/bash
# $1 is the setenv file to be source'd
# $2 is the XML configuration file
# $3 is the index of the command to be executed
# $4 is the data directory in the shared file system (that contains the images)
# $5 is the execution dir in the nodes
# $6 is the output folder in the shared file system

source $1
python $2 $3 $4 $5 $6
