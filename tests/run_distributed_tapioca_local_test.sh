#!/bin/bash
#
# Before running the test, add the following in include/XML_User/DicoCamera.xml:
# <CameraEntry>
#      <Name> Aquaris E5 HD </Name>
#      <SzCaptMm> 3.52 4.69 </SzCaptMm>
#      <ShortName> Aquaris E5 HD </ShortName>
# </CameraEntry>
set -e

micmac-disttapioca-create-pairs -i . -f jpg -o ImagePairs.xml
micmac-disttapioca-create-config -i ImagePairs.xml -o DistributedTapioca.xml -f DistributedTapioca -n 6
coeman-par-local -d . -e DistributedTapiocaExe -c DistributedTapioca.xml -n 2
micmac-disttapioca-combine -i DistributedTapiocaExe -o Homol

# Test if we produced expected output files
_match_count=$(ls Homol/Pastis?.jpg/*.dat |wc -w)
if [ $_match_count -ne 30 ]
then
    exit 1
fi
