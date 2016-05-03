import os
from pymicmac.pipeline import run_original

#ppfree,affineFree,drMax
testNames = (
"Original_0_0_0" ,
)

for testName in testNames:
    (_, ppfree,affineFree,drMax) = testName.split('_')
    run_original.run(testName, "JPG", ppfree, affineFree, drMax, 'coord_List2D.xml', 'gcp_List3D.xml', '/media/data', False)
