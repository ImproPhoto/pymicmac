# pymicmac
pymicmac provides a python interface, CPU/MEM/disk monitoring and distributed computing tools for MicMac.

MicMac is a photogrammetric suite which contains many different tools to execute photogrammetric workflows.
In short, a photogrammetric workflow contains at least:

 - (1) tie-point detection: extraction of key features in images and cross-match between different images to detect tie-points (points in the images that represent the same physical locations).

 - (2) Estimation of camera positions and orientations and of calibration parameters: mainly the bundle adjustment but may include some preparation and/or refinement steps.

 - (3) Dense-matching point cloud generation. 3D projection of image pixels to produce the dense point cloud.

pymicmac provides a python tool (`workflow/run_workflow.py`) to run photogrammetric workflows with a sequence of MicMac commands. The tool is configured with a XML that defines a chain of MicMac commands to be executed sequentially. Each of the commands is executed together with a CPU/MEM/disk monitor. The tool can be configured to run a whole photogrammetric workflow at once, or to run it split in pieces (recommended), for example by (1) tie-point detection, (2) parameters estimation and (3) matching.  More information in [Instructions](#instructions) section.

In section [Large image sets](#large-image-sets) we provide some tips on how to use MicMac and pymicmac for processing large image sets using distributed computing (for (1) tie-point detection and (3) matching) and tie-points reduction (for (2) parameters estimation).

## Installation

Clone this repository and install it with pip (using a virtualenv is recommended):

```
git clone https://github.com/ImproPhoto/pymicmac.git
cd pymicmac
pip install .
```

Python dependencies: noodles (see https://github.com/NLeSC/noodles for installation instructions)

Other python  dependencies (numpy, tabulate, matplotlib, lxml) are automatically installed by `pip install` but some system libraries have to be installed (for example freetype is required by matplotlib and may need to be installed by the system admin)

For now pymicmac works only in Linux systems. Requires Python 3.5.

## Instructions

The tool `workflow/run_workflow.py` is used to execute entire photogrammetric workflows with MicMac or portions of it. We recommend splitting the workflow in three pieces: (1) tie-point detection, (2) parameters estimation and (3) matching. Each time the tool is executed, it creates an independent execution folder to isolate the processing from the input data. The tool can be executed as a python script (see example in `tests/run_test.sh`) or can be imported as a python module (see examples in `tests/run_tiepoint_detection_example.py`, `tests/run_param_estimation_example.py` and `tests/run_matching_example.py`).

To configure the tool:
-  which images are used is specified with an ASCII file containing the list of files (one image path per line) if the tool is run as a script or with a python list/tuple with the images paths if the tool is imported.
When executing the tool and before executing the specified MicMac processes, an independent execution folder is created and (soft) links of all the specified images are created.
- which MicMac commands are executed is specified with a XML. The CPU/MEM/disk usage for each tool will be monitored. For each executed command some monitoring files are created in the execution folder. Concretely a .mon file, a .mon.disk and a .log file. The first one contains CPU/MEM usage monitoring, the second one contains disk usage monitoring and the third one is the log produced by the executed command. To get statistics of .mon files use `monitor/get_monitor_nums.py` and to get a plot use `monitor/plot_cpu_mem.py`. To plot the .mon.disk use `monitor/plot_disk.py`. In the `logsparser` and `logsplotter` packages there are tools to extract information and do plots from the log files of some of the commands (currently of `RedTieP`, `Tapas`, `Campari` and `GCPBascule`).

### XML configuration file

The XML file must contain a root tag `<MicMacConfiguration>`. Then, for each component/command of the chain we have to add a XML element `<Component>` which must have as child elements at least a `<id>` and a `<command>` elements.

Since the tool will be executed in an independent execution folder, if a component requires some files/folders other the images,
the required files/folders have to be specified with `<require>` element (if a previous tool in the chain already 'linked' a file/folder there is no need to do it again). (Soft) links will be created in the execution folder for the specified files/folders. For example, the first tool of the parameters estimation chain must for sure link to the Homol folder generated in the tie-points detection.

There is a special case for the `RedTieP` tool which may be used in during parameters estimation. If the component is `RedTieP` and `ExpSubCom=1` is specified as option, this means Noodles needs to run, then please specify the number of processes to use with the XML element `<noodlesNumProc>`. See example in `tests/estimation_workflow_tiepoint_reduction.xml`.

Some XML examples:

- Tie-points detection:
```
<MicMacConfiguration>
  <Component>
    <id> Tapioca </id>
    <command> mm3d Tapioca All ".*jpg" -1 </command>
  </Component>
</MicMacConfiguration>

```

- Parameter estimation:
```
<MicMacConfiguration>
  <Component>
    <id> Tapas </id>
    <command> mm3d Tapas Fraser ".*jpg" Out=TapasOut </command>
    <require>tie-point-detection/Homol</require>
  </Component>
</MicMacConfiguration>
```

- Matching:
```
<MicMacConfiguration>
  <Component>
    <id> Malt </id>
    <command> mm3d Malt GeomImage ".*jpg" TapasOut "Master=1.jpg" "DirMEC=Results" UseTA=1 ZoomF=1 ZoomI=32 Purge=true </command>
    <require> param-estimation/Ori-TapasOut</require>
  </Component>
  <Component>
    <id> Nuage2Ply </id>
    <command> mm3d Nuage2Ply "./Results/NuageImProf_STD-MALT_Etape_8.xml" Attr="1.jpg" Out=1.ply</command>
  </Component>
</MicMacConfiguration>
```

Following the examples above, we could execute a whole workflow with:
```
python pymicmac/workflow/run_workflow.py -i list.txt -e tie-point-detection -c tie-point-detection.xml
python pymicmac/workflow/run_workflow.py -i list.txt -e param-estimation -c param-estimation.xml
python pymicmac/workflow/run_workflow.py -i list.txt -e matching -c matching.xml
```

## Large image sets

For the (1) tie-point detection and (3) matching the processing can be easily enhanced by using distributed computing (clusters or clouds). The reason is that the processes involved can be easily split in independent chunks (in each chunk one or more images are processed). For the (2) parameters estimation, this is not the case since the involved processes usually require having data from all the images simultaneously in memory. In this case, we propose to use tie-points reduction to deal with large image sets.

For more information about distributed computing and tie-points reduction, see our paper (in preparation).

### Distributed computing

TBD

### Tie-points reduction

Add a tie-point reduction component in the chain for parameters estimation.

Two tools can be used for this purpose: `RedTieP` and `OriRedTieP`. The first one requires to run the tool `NO_AllOri2Im` before and the second requires to run the tool `Martini` before.

For examples, see `tests/param-estimation_reduction.xml` and  `tests/param-estimation_orireduction.xml`

When a tie-point reduction is used with either of the available tools, the tool `other/get_homol_diff.py` can be used to compute the reduction factors.
