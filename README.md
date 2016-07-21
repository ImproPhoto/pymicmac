# pymicmac
pymicmac provides a python interface, CPU/MEM/disk monitoring and distributed computing tools for MicMac.

MicMac is a photogrammetric suite which contains many different tools to execute photogrammetric workflows.
In short, a photogrammetric workflow contains at least:

 - (1) tie-point detection: extraction of key features in images and cross-match between different images to detect tie-points (points in the images that represent the same physical locations).

 - (2) Estimation of camera positions and orientations and of calibration parameters: mainly the bundle adjustment but may include some preparation and/or refinement steps.

 - (3) Dense-matching point cloud generation. 3D projection of image pixels to produce the dense point cloud.

pymicmac provides a python tool (`workflow/run_workflow.py`) to run photogrammetric workflows with a sequence of MicMac commands. The tool is configured with a Workflow XML configuration file that defines a chain of MicMac commands to be executed sequentially. Each of the commands is executed together with a CPU/MEM/disk monitor. The tool can be configured to run a whole photogrammetric workflow at once, or to run it split in pieces (recommended), for example by (1) tie-point detection, (2) parameters estimation and (3) matching.  More information in [Instructions](#instructions) section.

In section [Large image sets](#large-image-sets) we provide some tips on how to use MicMac and pymicmac for processing large image sets using distributed computing (for (1) tie-point detection and (3) matching) and tie-points reduction (for (2) parameters estimation).

## Installation

Clone this repository and install it with pip (using a virtualenv is recommended):

```
git clone https://github.com/ImproPhoto/pymicmac.git
cd pymicmac
pip install .
```

Python dependencies: noodles (see https://github.com/NLeSC/noodles for installation instructions)

Other python  dependencies (numpy, tabulate, matplotlib, lxml, pandas) are automatically installed by `pip install .` but some system libraries have to be installed (for example freetype is required by matplotlib and may need to be installed by the system admin)

For now pymicmac works only in Linux systems. Requires Python 3.5.

## Instructions

The tool `workflow/run_workflow.py` is used to execute entire photogrammetric workflows with MicMac or portions of it. We recommend splitting the workflow in three pieces: (1) tie-point detection, (2) parameters estimation and (3) matching. Each time the tool is executed, it creates an independent execution folder to isolate the processing from the input data. The tool can be executed as a python script (see example in `tests/run_test.sh`) or can be imported as a python module (see examples in `tests/run_tiepoint_detection_example.py`, `tests/run_param_estimation_example.py` and `tests/run_matching_example.py`).

Which MicMac commands are executed is specified with a Workflow XML configuration file. The CPU/MEM/disk usage for each tool will be monitored.

### Workflow XML configuration file

To configure the tool:
-  which images are used is specified with an ASCII file containing the list of files (one image path per line) if the tool is run as a script or with a python list/tuple with the images paths if the tool is imported.
When executing the tool and before executing the specified MicMac processes, an independent execution folder is created and (soft) links of all the specified images are created.
-

The Workflow XML configuration file file must contain a root tag `<Workflow>`. Then, for each component/command of the workflow we have to add a XML element `<Component>` which must have as child elements at least a `<id>` and a `<command>` elements.

Since the workflow will be executed in an independent execution folder, if a component requires some files/folders, the required files/folders have to be specified with `<require>` or `<requirelist>` tags. (Soft) links are created in the execution folder for the specified files/folders. Using `<require>` is for short list of required files/folders and they are specified comma-separated. Using `<requirelist>` is when the list of required files/folders is very long, in which case theya re specified ina  separate ASCII file, one file/folder per line. Both `<require>` and `<requirelist>` can be simultaneously used.  For example, the first tool of the parameters estimation chain must for sure link to the list of images and to the Homol folder generated in the tie-points detection. So, we can use `<requirelist>` to specify a list of images, and `<require>` for the Homol folder (or specify all in the `<requirelist>`).

It is important to notice that since all the commands of the workflow are executed in the same execution folder, if a previous tool in the workflow already 'linked' a file/folder (using `<require>` or `<requirelist>`) there is no need to do it again. So, only the first command in the workflow must link the images.

Some XML examples:

- Tie-points detection:
```
<Workflow>
  <Component>
    <id> Tapioca </id>
    <requirelist>list.txt</requirelist>
    <command> mm3d Tapioca All ".*jpg" -1 </command>
  </Component>
</Workflow>
```

- Parameter estimation:
```
<Workflow>
  <Component>
    <id> Tapas </id>
    <requirelist>list.txt</requirelist>
    <require>tie-point-detection/Homol</require>
    <command> mm3d Tapas Fraser ".*jpg" Out=TapasOut </command>
  </Component>
</Workflow>
```

- Matching:
```
<Workflow>
  <Component>
    <id> Malt </id>
    <requirelist>list.txt</requirelist>
    <require> param-estimation/Ori-TapasOut</require>
    <command> mm3d Malt GeomImage ".*jpg" TapasOut "Master=1.jpg" "DirMEC=Results" UseTA=1 ZoomF=1 ZoomI=32 Purge=true </command>
  </Component>
  <Component>
    <id> Nuage2Ply </id>
    <command> mm3d Nuage2Ply "./Results/NuageImProf_STD-MALT_Etape_8.xml" Attr="1.jpg" Out=1.ply</command>
  </Component>
</Workflow>
```

Following the examples above, we could execute a whole workflow with:
```
python pymicmac/workflow/run_workflow.py -e tie-point-detection -c tie-point-detection.xml
python pymicmac/workflow/run_workflow.py -e param-estimation -c param-estimation.xml
python pymicmac/workflow/run_workflow.py -e matching -c matching.xml
```

### Monitoring

For each executed command of the specified in the Workflow XML configuration file the CPU, memory and disk usage are monitored. Some monitoring files are created in the execution folder. Concretely a .mon file, a .mon.disk and a .log file. The first one contains CPU/MEM usage monitoring, the second one contains disk usage monitoring and the third one is the log produced by the executed command. To get statistics of .mon files use `monitor/get_monitor_nums.py` and to get a plot use `monitor/plot_cpu_mem.py`. To plot the .mon.disk use `monitor/plot_disk.py`. In the `logsparser` and `logsplotter` packages there are tools to extract information and do plots from the log files of some of the commands (currently of `RedTieP`, `Tapas`, `Campari` and `GCPBascule`).

## Large image sets

For the (1) tie-point detection and (3) matching the processing can be easily enhanced by using distributed computing (clusters or clouds). The reason is that the processes involved can be easily split in independent chunks (in each chunk one or more images are processed). For the (2) parameters estimation, this is not the case since the involved processes usually require having data from all the images simultaneously in memory. In this case, we propose to use tie-points reduction to deal with large image sets.

For more information about distributed computing and tie-points reduction, see our paper (in preparation).

### Distributed computing

Some parts of the photogrammetric workflow, namely the tie-points detection and the matching, can be boosted by using distributed computing systems since the involved processes can be divided in chunks which are independent to process.

For example, the Tapioca tool (tie-points detection) first extracts the features for each image and then cross-matches the features between image pairs. The distributed computing solution that we propose is to divide the list of all image pairs in chunks where each chunk can be processed independently (though they may read sometimes the same images). The results from each chunk processing need to be combined.

To characterize the distributed computing of tools like Tapioca we use a Distributed Tool XML configuration file which is similar to the Workflow XML configuration file.

The Distributed Tool XML configuration file must contain a root tag `<DistributedTool>`. Then, for each chunk of the distributed tool we have to add a XML element `<Component>` which must have as child elements the `<id>` and a `<command>` elements. This is the same as the Workflow XML configuration file format. However, in this case each `<Component>` tag must also contain a `<output>`, which determines which files or folder are the output. Like in the Workflow XML configuration file format, `<requirelist>` and `<require>` are also used to define the required data by each command.

When running this distributed computing workflow each command is executed in a different execution folder and possibly in a different computer. For each command, the required data is copied from the location where the workflow run is lunched to the remote execution folder, and then the command is executed. When the command is finished the elements indicated in `<output>` are copied back to the location where the workflow run was lunch.

Note that in this case, the data indicated by `<require>` and `<requirelist>` is not shared between different commands execution. So, in each command `<require>` and `<requirelist>` must indicate ALL the required data. This is different than in the Worflow execution where the required data can be shared by other commands since they are all executed in the same execution folder.

An example Distributed Tool XML configuration file follows. In this case, we have divided Tapioca processing in two chunks. Each chunk processes the half of the image pairs:

```
<DistributedTool>
  <Component>
    <id>0_Tapioca</id>
    <requirelist>DistributedTapioca/0_ImagePairs.xml.list</requirelist>
    <require>DistributedTapioca/0_ImagePairs.xml</require>
    <command>mm3d Tapioca File 0_ImagePairs.xml -1</command>
    <output>Homol</output>
  </Component>
  <Component>
    <id>1_Tapioca</id>
    <requirelist>DistributedTapioca/1_ImagePairs.xml.list</requirelist>
    <require>DistributedTapioca/1_ImagePairs.xml</require>
    <command>mm3d Tapioca File 1_ImagePairs.xml -1</command>
    <output>Homol</output>
  </Component>
</DistributedTool>
```

How the data is copied from the location where the distributed tool is lunched to the remote execution folders (and viceversa) depends on the used hardware systems.

In [Implemented MicMac Tools](#implemented-micmac-tools) we detail the current MicMac tools where we have implemented a distributed version. Currently Tapioca is supported.

In [Hardware systems](#hardware-systems) we detail which systems are supported. Currently running in SGE clusters is supported. SGE clusters have Grid Engine batch queueing system.

#### Implemented MicMac Tools

##### Tapioca

The folder `workflow/distributed_tapioca` contains tools to run Tapioca using distributed computing systems.

First, in order to run this tool we need a image pairs file. This file list the image pairs that need to be considered when running Tapioca. This is very helpful to avoid running Tapioca with every possible image pair. If you do not have a image pairs file, you can use the tool `workflow/distributed_tapioca/create_all_image_pairs_file.py` to create a image pairs file with every possible image pair.

Second, we use the `workflow/distributed_tapioca/create_tapioca_distributed_tool_config_file.py` to split the image pairs XML file in multiple chunks and to create a Distributed Tool XML configuration file:

```
python [path to pymicmac]/pymicmac/workflow/distributed_tapioca/create_tapioca_distributed_tool_config_file.py -i [input XML image pairs] -f [folder for output XMLs and file lists, one for each chunk] -n [number of image pairs per output XML, must be even number] -o [Distributed Tool XML configuration file]
```

Depending in the maximum job execution time of the cluster you are using, chose a number wisely. For example, we chose 20 image pairs per chunk to have jobs that last less than 10 minutes.

Now, you are ready to run this distributed tool in any of the available hardware systems that are supported by pymicmac (see [Hardware systems](#hardware-systems)).

After the distributed Tapioca has finished you will have to combine all the outputs from the different chunks. Use `workflow/distributed_tapioca/combine_distributed_tapioca_output.py` to join them into a final Homol folder

```
python [path to pymicmac]/workflow/distributed_tapioca/combine_distributed_tapioca_output.py -i [folder with subfolders, each subfolder with the results of the processing of a chunk] -o [output combined folder]
```

#### Hardware systems:

##### SGE clusters

The tools in `workflow/run_distributed_tool_sge_cluster` is used to run Distributed Tool specified by Ditributed Tool XML configuration files in SGE clusters.

SGE cluster usually have a shared folder where all the nodes can access. However, since massive simultaneous access to the shared folder is discouraged, usually local storage in the execution nodes is used when possible.

In our case, both the images and the required data must be in a location that can be accessed from all the cluster nodes computers.

After a Distribution Tool configuration file has been created, the tool `workflow/run_distributed_tool_sge_cluster/create_distributed_tool_sge_jobs.py` creates the submission script. This tool requires to specify the data directory, a setenv file and local output directory. All these files and folders and the XML configuration file must be in a shared folder. The tool also requires to specify a remote execution directory. This is the directory in each remote node where the execution of the commends will be done. To submit the different jobs to the queueing system, run the the produced submission script.


### Tie-points reduction

Add a tie-point reduction component in the chain for parameters estimation.

Two tools can be used for this purpose: `RedTieP` and `OriRedTieP`. The first one requires to run the tool `NO_AllOri2Im` before and the second requires to run the tool `Martini` before.

For examples, see `tests/param-estimation_reduction.xml` and  `tests/param-estimation_orireduction.xml`

When a tie-point reduction is used with either of the available tools, the tool `other/get_homol_diff.py` can be used to compute the reduction factors.

Note that after running the tie-points reduction tools, the Homol folder has to be changed (see the examples).
Also note that when running `RedTieP`, it is possible to use parallel execution mode. See the example in `tests/param-estimation_reduction.xml`.
