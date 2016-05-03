import os
from pymicmac.pipeline import run_reduced

#nX,nY,adaptive,gain_mode,threshold,ordering
testNames = (
# "TPR_12_12_0_1_0.0_0",
# "TPR_20_20_0_1_0.0_0",
"TPR_8_8_0_1_0.0_0" ,
"TPR_10_10_0_1_0.0_0",
"TPR_14_14_0_1_0.0_0" ,
"TPR_16_16_0_1_0.0_0",
"TPR_18_18_0_1_0.0_0" ,
)

for testName in testNames:
    (_, nX, nY, adaptive, gain_mode, threshold, ordering) = testName.split('_')
    run_reduced.run(testName, "JPG", nX, nY, adaptive, gain_mode, threshold, ordering, 'coord_List2D.xml', 'gcp_List3D.xml', 4, '/media/data', False)
