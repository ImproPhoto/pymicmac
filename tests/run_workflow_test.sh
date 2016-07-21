#!/bin/bash
#
# Before ruuning the test, add the following in include/XML_User/DicoCamera.xml:
# <CameraEntry>
#      <Name> Aquaris E5 HD </Name>
#      <SzCaptMm> 3.52 4.69 </SzCaptMm>
#      <ShortName> Aquaris E5 HD </ShortName>
# </CameraEntry>

python ../pymicmac/workflow/run_workflow.py -d . -e tie-point-detection -c tie-point-detection.xml
python ../pymicmac/workflow/run_workflow.py -d . -e param-estimation -c param-estimation.xml
# python ../pymicmac/workflow/run_workflow.py -d . -e param-estimation-red -c param-estimation_reduction.xml
# python ../pymicmac/workflow/run_workflow.py -d . -e param-estimation-orired -c param-estimation_orireduction.xml
python ../pymicmac/workflow/run_workflow.py -d . -e matching -c matching.xml
