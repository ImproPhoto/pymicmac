#!/bin/bash
set -e
echo "Checking dependencies..."
echo "ImageMagick:"
convert --version
echo "exiv2:"
exiv2 --version
echo "exiftool:"
exiftool --version

echo "micmac-run-workflow -d . -e tie-point-detection -c tie-point-detection.xml"
micmac-run-workflow -d . -e tie-point-detection -c tie-point-detection.xml
echo "micmac-run-workflow -d . -e param-estimation -c param-estimation.xml"
micmac-run-workflow -d . -e param-estimation -c param-estimation.xml
echo "micmac-run-workflow -d . -e param-estimation-red -c param-estimation_reduction.xml"
micmac-run-workflow -d . -e param-estimation-red -c param-estimation_reduction.xml
echo "micmac-run-workflow -d . -e param-estimation-orired -c param-estimation_orireduction.xml"
micmac-run-workflow -d . -e param-estimation-orired -c param-estimation_orireduction.xml
echo "micmac-run-workflow -d . -e matching -c matching.xml"
micmac-run-workflow -d . -e matching -c matching.xml
echo "done."
