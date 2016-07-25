#!/bin/bash
#
# Before ruuning the test, add the following in include/XML_User/DicoCamera.xml:
# <CameraEntry>
#      <Name> Aquaris E5 HD </Name>
#      <SzCaptMm> 3.52 4.69 </SzCaptMm>
#      <ShortName> Aquaris E5 HD </ShortName>
# </CameraEntry>

python ../pymicmac/workflow/distributed_tapioca/create_all_image_pairs_file.py -i . -f jpg -o ImagePairs.xml
python ../pymicmac/workflow/distributed_tapioca/create_parcommands_config_file.py -i ImagePairs.xml -o DistributedTapioca.xml -f DistributedTapioca -n 6
python -c "from pycoeman.parcommands import run_parcommands_local; run_parcommands_local.run('.', 'DistributedTapiocaExe', 'DistributedTapioca.xml', 2, False)"
python ../pymicmac/workflow/distributed_tapioca/combine_distributed_tapioca_output.py -i DistributedTapiocaExe -o Homol
