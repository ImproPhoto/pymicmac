#!/bin/bash
#
# Before ruuning the test, add the following in include/XML_User/DicoCamera.xml:
# <CameraEntry>
#      <Name> Aquaris E5 HD </Name>
#      <SzCaptMm> 3.52 4.69 </SzCaptMm>
#      <ShortName> Aquaris E5 HD </ShortName>
# </CameraEntry>

python ../pymicmac/workflow/run_workflow.py -i list.txt -e tie-point-detection -c tie-point-detection.xml
python ../pymicmac/workflow/run_workflow.py -i list.txt -e param-estimation -c param-estimation.xml
python ../pymicmac/workflow/run_workflow.py -i list.txt -e matching -c matching.xml
