import os
from pymicmac.pipeline import run_ori_reduced

#Prec2P,SzTile,DistPMul,MVG
testNames = (
"OTPR_20.0_2000_175_1.5",
"OTPR_20.0_2000_100_1.5",
)

for testName in testNames:
    (_, prec,sizeTile,distMul,multiVG) = testName.split('_')
    run_ori_reduced.run(testName, "JPG", prec, sizeTile, distMul, multiVG, 'coord_List2D.xml', 'gcp_List3D.xml', '/media/data', False)
