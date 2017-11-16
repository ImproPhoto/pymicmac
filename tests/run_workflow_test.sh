#!/bin/bash
set -e
echo "Checking dependencies..."
echo "ImageMagick:"
convert --version
echo "exiv2:"
exiv2 --version
echo "exiftool:"
exiftool -ver

echo "micmac-run-workflow -d . -e tie-point-detection -c tie-point-detection.xml"
micmac-run-workflow -d . -e tie-point-detection -c tie-point-detection.xml
echo "micmac-run-workflow -d . -e param-estimation -c param-estimation.xml"
micmac-run-workflow -d . -e param-estimation -c param-estimation.xml

#The following commands are not executed because of the issue "run_workflow_test.sh test fails #36"
#echo "micmac-run-workflow -d . -e param-estimation-red -c param-estimation_reduction.xml"
#micmac-run-workflow -d . -e param-estimation-red -c param-estimation_reduction.xml
#echo "micmac-run-workflow -d . -e param-estimation-orired -c param-estimation_orireduction.xml"
#micmac-run-workflow -d . -e param-estimation-orired -c param-estimation_orireduction.xml

echo "micmac-run-workflow -d . -e matching -c matching.xml"
micmac-run-workflow -d . -e matching -c matching.xml

# Test if we produced expected ply model
_match_count=$(matching/1.ply |wc -w)
if [ $_match_count -ne 1 ]
then
    echo 'Test failed, output ply file wasn't produced.'
    exit 1
fi

echo "done."
