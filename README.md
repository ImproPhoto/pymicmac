# pymicmac
Python tools for the MicMac FOSS photogrammetric "suite". It works only in Linux systems.

##Instructions
1- Use pipeline/run_tapioca.py to run the tie-point detection and matching. This requires the image files in the local folder. The output will be a Homol folder with the tie-points
2- Use any of the pipeline scripts to run the rest of the pipeline. This will create a "pipeline" folder for the pipeline run and create soft-links to the images and Homol folder. All the results will be written in the "pipeline" folder
