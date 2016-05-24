# pymicmac
Python tools for the MicMac FOSS photogrammetric "suite". It works only in Linux systems.

##Instructions
1- Use workflow/run_tiepoint_detection.py to run the tie-point detection and matching. This requires the image files in the local folder. The output will be a Homol folder with the tie-points. See example of how to run it in tests/run_tapioca.py

2- Now you need to compose a photogrammetric workflow and run workflow/run_param_estimation.
   The workflow is configured through a XML file. For examples see the XML files in tests folder.
   This will create a "workflow" folder for the workflow run and create soft-links to the images, Homol and other links as specified in the XML.
   All the results will be written in the "workflow" folder

##MicMac parameter estimation XML file
The XML file to run parameter estimation with MicMac is for example:
```
<MicMacConfiguration>
  <Component>
    <name> Tapas </name>
    <options> Fraser ".*JPG" InCal=IniCal Out=TapasOut </options>
    <toLink> Ori-IniCal </toLink>
  </Component>
  <Component>
    <name> GCPBascule </name>
    <options> ".*JPG" TapasOut GCPBOut gcp_List3D.xml coord_List2D.xml </options>
    <toLink> gcp_List3D.xml coord_List2D.xml </toLink>
  </Component>
</MicMacConfiguration>
```

For each component of the workflow (in the example Tapas and GCPBascule) we have to add
a XML element `<Component>` which must have as child elements at least a `<name>` and a `<options>` elements.
If the component requires some file/folder other than the Homol folder and the images,
the required files have to be specified with `<toLink>` element.
If the component is `RedTieP` and `ExpSubCom=1` is specified as option, which means Noodles needs to run, then please specify the number of processes to use with the XML element `<noodlesNumProc>`
