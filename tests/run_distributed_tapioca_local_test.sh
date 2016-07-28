#!/bin/bash
#
# Before ruuning the test, add the following in include/XML_User/DicoCamera.xml:
# <CameraEntry>
#      <Name> Aquaris E5 HD </Name>
#      <SzCaptMm> 3.52 4.69 </SzCaptMm>
#      <ShortName> Aquaris E5 HD </ShortName>
# </CameraEntry>

micmac-disttapioca-create-pairs -i . -f jpg -o ImagePairs.xml
micmac-disttapioca-create-config -i ImagePairs.xml -o DistributedTapioca.xml -f DistributedTapioca -n 6
coeman-par-local -d . -e DistributedTapiocaExe -c DistributedTapioca.xml -n 2
micmac-disttapioca-combine -i DistributedTapiocaExe -o Homol
