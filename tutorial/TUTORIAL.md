# Tutorial

This tutorial is intended to drive you in the process to convert a bunch of images in some folder of your (Linux) computer into a colored dense point cloud using MicMac and pymicmac.

## Installation

Before anything else, we need to install all the required software: MicMac and pymicmac and their dependencies.
In this tutorial, we do the installation on Ubuntu 16.04. Note that some steps and libraries names may be different in other Linux distributions.

First, we install MicMac (we get MicMac from its SVN repository):
```
# Install mercurial to be able to download MicMac
sudo apt-get install mercurial

# We install it in the next location (please change accordingly to your system)
cd /home/oscar/sw

# Clone the repo (this requires user/password)
hg clone https://geoportail.forge.ign.fr/hg/culture3d

# Install MicMac
cd culture3d
mkdir build
cd build
cmake ..
make -j24
make install

# Assuming that we installed micmac in /home/oscar/sw/culture3d, add the next lines to your .bashrc (in your case replace accordingly)
export LD_LIBRARY_PATH="/home/oscar/sw/culture3d/lib:$LD_LIBRARY_PATH"
export PATH="/home/oscar/sw/culture3d/bin:$PATH"

# Source .bashrc to activate the installation
source ~/.bashrc
```

Second, pymicmac is a Python 3.5 package so we need to have a Python 3.5 installation. We recommend using Anaconda:
```
# Get the latest Anaconda installer (in 32 or 64 bits depending on your system)
wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh

# Install it
bash Anaconda3-4.2.0-Linux-x86_64.sh

# Create a anaconda environment for all the installation of pymicmac
conda create --name python35 python=3.5

# Add this line in your .bashrc
source activate python35

# Source .bashrc to activate the installation
source ~/.bashrc
```

Third, pymicmac has some system library requirements (freetype, ssl, ffi) and also requires pycoeman and noodles:
```
# Install pycoeman dependencies
sudo apt-get install libfreetype6-dev libssl-dev libffi-dev

# Install pycoeman
pip install git+https://github.com/NLeSC/pycoeman

# Install noodles
pip install git+https://github.com/NLeSC/noodles
```

Finally, we install pymicmac:
```
# Install pymicmac
pip install git+https://github.com/ImproPhoto/pymicmac
```

We can test the installation:
```
mm3d -help
micmac-run-workflow -h
```

## Processing a dataset

Now that we have all performed the installation of all tne required software, we will generate a colored dense point cloud.
We assume that the data is in `/home/oscar/data/GRONAU/4ms_60m_1000`. Concretely the folder looks like:

```
ls /home/oscar/data/GRONAU/4ms_60m_1000
coord_List2D.xml gcp_List3D.xml GrapheHom.xml Ori-IniCal
IMG_0990.JPG ...
```

In addition to the set of JPG images, we also have GCPs files, a `GrapheHom.xml` file and a `Ori-IniCal` folder.
The GCPs file `gcp_List3D.xml` have the 3D positions of the Ground Control Points (GCPs) and Check Points (CPs), and their 2D positions in the images are registered in the `coord_List2D.xml` file. The `GrapheHom.xml` contains the list of valid image pairs (extracted from geotag info). The `Ori-IniCal` folder contains a XML file with the initial calibration information.

For pymicmac it will make our live easier if we create a file with the list of images:
```
cd /home/oscar/data/GRONAU/4ms_60m_1000
ls *JPG > images.list
```

Our photogrammetric pipeline with MicMac consists of running Tapioca to extract tie-points, followed by Tapas to perform the bundle block adjustment, and finally Malt, Tawny and Nuage2Ply to get the colored dense point cloud.

The commands to be executed are configured in pymicmac with XML. During execution, the commands are executed in a folder than the one where the original data is stored. For the required data links are created. pymicmac monitors the CPU/MEM and disk usage. With pymicmac we can configure any photogrammetric workflow and we can split it in parts in any way we want. In the next subsections, we present a couple of examples of different strategies to execute workflows.

### Single XML with entire workflow
In this example we define a single XML to execute the entire workflow. The pymicmac XML configuration file is called `Workflow.xml` and its content is:
```
<SeqCommands>
  <Component>
    <id> Tapioca </id>
    <require> GrapheHom.xml </require>
    <requirelist> images.list </requirelist>
    <command> mm3d Tapioca File GrapheHom.xml -1 </command>
  </Component>
  <Component>
    <id> Tapas </id>
    <command> mm3d Tapas Fraser ".*JPG" InCal=IniCal Out=TapasOut </command>
    <require> Ori-IniCal </require>
  </Component>
  <Component>
    <id> GCPBascule </id>
    <command> mm3d GCPBascule ".*JPG" TapasOut GCPBOut gcp_List3D.xml coord_List2D.xml </command>
    <require> gcp_List3D.xml coord_List2D.xml </require>
  </Component>
  <Component>
    <id> Malt </id>
    <command> mm3d Malt Ortho ".*JPG" GCPBOut </command>
  </Component>
  <Component>
    <id> Tawny </id>
    <command> mm3d Tawny Ortho-MEC-Malt </command>
  </Component>
  <Component>
    <id> Nuage2Ply </id>
    <command> mm3d Nuage2Ply MEC-Malt/NuageImProf_STD-MALT_Etape_8.xml Attr=Ortho-MEC-Malt/Orthophotomosaic.tif Out=pointcloud.ply </command>
  </Component>
</SeqCommands>
```

The workflow is executed with pymicmac with:
```
cd /home/oscar/data/GRONAU/4ms_60m_1000/
micmac-run-workflow -d . -c Workflow.xml -e WorkflowOutput
```

Note that in each command the required files/folders are specified with the tags `<require>` and `<requirelist>`. The specified locations are relative paths to the folder specified in the `-d` option of the `micmac-run-workflow` command, i.e. `.` which is `/home/oscar/data/GRONAU/4ms_60m_1000/`. Also note that there is no need to duplicate required items. For example, all the commands need the images (provided with `<requirelist>`) but it is enough to specify this in the first command.

Executing `micmac-run-workflow` will first create the `WorkflowOutput` folder, then it will create links inside this folder to all the required data (specified with `<require>` and `<requirelist>`) and finally will run all the commands. After the execution is finished, for each of the commands we will find in `WorkflowOutput` a log file, a mon file and and mon.disk file. These contain respectively the log of the command execution, the CPU/MEM usage and the disk usage.
pycoeman has tools to obtain statistics of the CPU/MEM usage:
```
coeman-mon-stats -t Tapioca,Tapas,GCPBascule,Malt,Tawny,Nuage2Ply -f WorkflowOutput
```


### Various XMLs to (re-)execute parts of the workflow
While the previous example is useful, one can argue if only to have CPU/MEM/disk usage and a clean environment it is worthy the hassle to install and learn how to operate pymicmac, and that is a completely valid point. However, it is not for cases like the previous one that pymicmac was made.

In this second example we will see when pymicmac is really beneficial. Now we want to run a workflow similar to the previous one but with a tie-points reduction step before Tapas. This will make Tapas execution faster. We also want to compare the workflow with tie-points reduction with the case when no reduction is used. More concretely we will look at the residuals of Tapas and the the errors of GCPBascule. We would also like to see the impact of Tapas if reduction is used (less memory and faster execution)

Running Tapioca is common in the two workflows we want to test. Thus, we divide the workflows in two parts. The first part is Tapioca and the second part is Tapas and GCPBascule with and without tie-points reduction. In this example, since we are only interested in Tapas and GCPBascule we will not run Malt, Tawny and Nuage2Ply.

The XML to run Tapioca is called `Tapioca.xml` and its content is:
```
<SeqCommands>
  <Component>
    <id> Tapioca </id>
    <require> GrapheHom.xml </require>
    <requirelist> images.list </requirelist>
    <command> mm3d Tapioca File GrapheHom.xml -1 </command>
  </Component>
</SeqCommands>
```

We execute it with:
```
cd /home/oscar/data/GRONAU/4ms_60m_1000/
micmac-run-workflow -d . -c Tapioca.xml -e TapiocaOutput
```

This will create the `TapiocaOutput` folder, make links to the images and to the `GrapheHom.xml` file and will execute Tapioca inside `TapiocaOutput`. When execution is finished, in addition to the `Homol` created by Tapioca, we will also have a log file, a mon file and a mon.disk. We can use `coeman-mon-stats` to get a overview on the CPU/MEM usage of Tapioca:
```
coeman-mon-stats -t Tapioca -f TapiocaOutput
```

Next, we define the rest of the workflow when no tie-points reduction is done. The `WorkflowNoTPR.xml` is:
```
<SeqCommands>
  <Component>
    <id> Tapas </id>
    <require> Ori-IniCal TapiocaOutput/Homol </require>
    <requirelist> images.list </requirelist>
    <command> mm3d Tapas Fraser ".*JPG" InCal=IniCal Out=TapasOut </command>
  </Component>
  <Component>
    <id> GCPBascule </id>
    <command> mm3d GCPBascule ".*JPG" TapasOut GCPBOut gcp_List3D.xml coord_List2D.xml </command>
    <require> gcp_List3D.xml coord_List2D.xml </require>
  </Component>
```

Note that in this case in Tapas we need to specify that we require `images.list` (we always do this in the first command in the XML) and that we also require the `Homol` folder. This will be inside the `TapiocaOutput` folder created before (which will be inside `/home/oscar/data/GRONAU/4ms_60m_1000/` so it is fine to use the relative path). We can now run the workflow with:
```
cd /home/oscar/data/GRONAU/4ms_60m_1000
micmac-run-workflow -d . -c WorkflowNoTPR.xml -e NoTPROutput
```

This will create the `NoTPROutput` folder, then it will create links to the images, the `Homol` folder and the rest of files, and finally will run Tapas and GCPBascule. Like before, after the execution is finished we will find log files, mon files and mon.disk files also in `NoTPROutput` folder.

Following we define the workflow with tie-points reduction. We can reuse the same `Homol`folder than before so there is not need to rerun Tapioca. The `WorkflowTPR.xml` is:
```
<SeqCommands>
  <Component>
    <id> NO_AllOri2Im </id>
    <require> TapiocaOutput/Homol </require>
    <requirelist> images.list </requirelist>
    <command> mm3d TestLib NO_AllOri2Im ".*JPG" Quick=1 </command>
  </Component>
  <Component>
    <id> RedTieP </id>
    <command> mm3d RedTiep ".*JPG" NumPointsX=12 NumPointsY=12  WeightAccGain=0.00; rm Homol; mv Homol-Red Homol </command>
  </Component>
  <Component>
    <id> Tapas </id>
    <require> Ori-IniCal </require>
    <command> mm3d Tapas Fraser ".*JPG" InCal=IniCal Out=TapasOut </command>
  </Component>
  <Component>
    <id> GCPBascule </id>
    <command> mm3d GCPBascule ".*JPG" TapasOut GCPBOut gcp_List3D.xml coord_List2D.xml </command>
    <require> gcp_List3D.xml coord_List2D.xml </require>
  </Component>
```

First NO_AllOri2Im will run (which is required by RedTiep, the tie-points reduction tool) and since this is the first command we add the requires for the images and the `Homol` folder. Next, the actual reduction with RedTieP will be done. Note that after the reduction we will replace the `Homol` folder with the one output by the tool. But do no panic!, the `rm Homol` only deletes the link to the `Homol` folder. The full set of tie-points is still there. This is one of the benefits of separating the execution of the several parts of the workflow and of using links. Finally, we will run Tapas and GCPBascule exactly as before but in this case they will use a reduced set of tie-points. We execute it with:
```
cd /home/oscar/data/GRONAU/4ms_60m_1000
micmac-run-workflow -d . -c WorkflowTPR.xml -e TPROutput
```

After the execution is done, we will find log files, mon files and mon.disk files in the `TPROutput` folder.

#### Comparison of workflows

We want to compare the results in the two workflows. First, we see the different CPU/MEM usage of the executed commands in both cases:
```
coeman-mon-stats -t Tapioca,NO_AllOri2Im,RedTieP,Tapas,GCPBascule -f TapiocaOutput,NoTPROutput,TPROutput
```
The output will look something like:
```
##########################
Time/CPU/MEM tools monitor
##########################
#Command     ExeFolder      Time[s]    Avail. CPU    Max. CPU    Mean CPU    Avail. MEM[GB]    Max. MEM[GB]    Mean MEM[GB]
----------   -----------  ---------  ------------  ----------  ----------  ----------------  --------------  --------------
Tapioca      TapiocaOutput   508433           400       400        384.42             13.13            3.44            1.78
NO_AllOri2Im TPROutput          607           400       182.8       38.64             13.13            3.11            2.86
RedTieP      TPROutput           91           400        87.1       14.76             13.13            3.05            2.8
Tapas        NoTPROutput      65199           400       266.4      100.28             13.13            9.18            8.82
Tapas        TPROutput         3154           400       321.9      111.54             13.13            4.73            3.46
GCPBascule   NoTPROutput          7           400       101.1       72.01             13.13            0.7             0.68
GCPBascule   TPROutput            6           400       104         88.84             13.13            1.61            1.59
```
Tapas when reduction is done is 30x faster and uses much less RAM. We can also see the actual reduction that has been done in tie-points set in the second workflow:
```
micmac-homol-compare -o TapiocaOutput/Homol -c NoTPROutput/Homol,TPROutput/Homol
```
The output will look like:
```
###########
Ratio Homol
###########
#Name                      Homol dec
-----------------------  -----------
NoTPROutput                   1.0000
TPROutput                     0.0669
```
Only 6.7% of the tie-points were used! But did the images correctly oriented with only 6.7% of the tie-points?.
Well, let's look at the Tapas residuals.
The tool `micmac-tapas-log-anal` opens the Tapas log files, counts the number of iterations and for the last one it shows the residuals:
```
micmac-tapas-log-anal -f NoTPROutput,TPROutput
```
will report something like:
```
##########################
Tapas last residuals/worts
##########################
#Name                NumIter       Res      Wor
-----------------  ---------  --------  -------
NoTPROutput              160  0.642464  1.83815
TPROutput                132  0.727202  1.02918
```
The residuals are a bit higher if tie-points reduction is applied. We could expect this. Note that less iterations were required with less tie-points. Next, we check what really happened with the GCPs points. The tool `micmac-gcpbascule-log-anal` reads the GCPBascule logs and computes the errors of the orientation in the GCPs.
```
micmac-gcpbascule-log-anal -x gcp_List3D.xml -f NoTPROutput,TPROutput
```
will report something like:
```
###########################
GCPBascule Dists statistics
###########################
KOs
#Name
-----------------  -----------------------
NoTPROutput        -
TPR_12_12_0.00_N   -

GCPs
#Name                 Min     Max    Mean     Std    Median
-----------------  ------  ------  ------  ------  --------
NoTPROutput        0.0419  0.1191  0.0799  0.0278    0.0681
TPROutput          0.0583  0.1182  0.096   0.0242    0.1101

CPs
#Name                 Min     Max    Mean     Std    Median
-----------------  ------  ------  ------  ------  --------
NoTPROutput        0.0231  0.2374  0.0888  0.051     0.0734
TPROutput          0.0287  0.2662  0.1048  0.0616    0.0785
```

The errors (in meters) of using a reduced set of tie-points increase less than 2 centimeters.

The previous example is the sort of case in which pymicmac will make your life much easier, i.e. when you have to rerun parts of the workflow with different parameters (or commands) and then you want to compare between the different workflows.



### What else can do pymicmac for you? Distributed computing

In the previous example we ran two workflows and we compared them. We saw that by using pymicmac the whole process is a bit less tedious.
In addition to the benefits highlighted in the previous example, there are tools in pymicmac that are crucial when processing large image sets.

We saw that we can use tie-points reduction to decrease the memory usage and to speed-up Tapas (the bundle block adjustment). But what happens with Tapioca and with the dense image matching (Malt, Tawny and Nuage2Ply)? We saw in one of the tables before that while Tapas without tie-points reduction took around 60,000 seconds, Tapioca took around 500,000 seconds. That is almost a week! And the dataset was not even that large, just a few hundred images. Tie-points reduction is useful to run Tapas with large sets faster and with less memory. However, with large image sets issues also arise in Tapioca and later also in the dense image matching. In these cases, a feasible choice is to use distributed computing facilities such as clouds or clusters. pymicmac has tools to run a distributed version of Tapioca and a distributed version of the dense image matching pipeline (Malt, Tawny, Nuage2Ply) in clusters (with SGE queuing system) and in a bunch of ssh-reachable machines. In order to port these tasks to distributed computing systems, a small modification in the algorithms that perform these tasks is required. The key idea is to divide the processing in chunks that can be processed independently (and in different machines), and combine the results in the end.

Next we show how to use these tools in a SGE cluster.

#### Distributed Tapioca

In this example, we have transfered the dataset used in the previous examples to a SGE cluster. We have stored the data in the following location `/var/scratch/orubi/data/medium/4ms_60m_1000`. This is a shared location, so all the nodes of the cluster can access it. The folder contains:
```
coord_List2D.xml gcp_List3D.xml GrapheHom.xml Ori-IniCal images.list
IMG_0990.JPG ...
```

In order to run the distributed Tapioca, first we need to divide the processing in chunks. The tool `micmac-disttapioca-create-config` can be used to define the different chunks and the processing that needs to be done for each chunk.
```
micmac-disttapioca-create-config -i GrapheHom.xml -o DistributedTapioca.xml -f ChunksData -n 50
```

The previous command divides the image pairs defined in `GrapheHom.xml` in chunks of 50 image pairs (if you do not have a file like `GrapheHom.xml` you can use `micmac-disttapioca-create-pairs` to create one with all possible image pairs). Which image pairs are used in each chunk is stored in files in the `ChunksData` folder. For each chunk it defines the commands to execute and all the commands are stored in `DistributedTapioca.xml`.

Now we use the tool `coeman-par-sge` in pycoeman to run the list of commands in the cluster and in parallel:
```
cd /var/scratch/orubi/data/medium/4ms_60m_1000
coeman-par-sge -d . -c DistributedTapioca.xml -s /home/orubi/sw/export_paths.sh -r /local/orubi/DistributedTapioca -o DistributedTapiocaAllOutputs
```
`/var/scratch/orubi/data/medium/4ms_60m_1000` is our shared data location, so all paths in the XML files are relative to this location. The various commands to run in the cluster are specified in `DistributedTapioca.xml`. The file `/home/orubi/sw/export_paths.sh` is a file that sets the environment in the nodes. Once a job is going to be executed in a certain node, the node needs to have the software available (MicMac, pymicmac and pycoeman). The execution of the jobs in the nodes will be done in the location specified, i.e. `/local/orubi/DistributedTapioca`. For each job the required data for the chunk will copied from the shared data location (`/var/scratch/orubi/data/medium/4ms_60m_1000`) to the local disk (`/local/orubi/DistributedTapioca`) so each job has a local copy of the required data for faster access. The chunk will be processed locally in the node and the output data (the partial `Homol` folders) will be copied back to the shared location.

Once all the jobs have finished (check qsub) we need to combined the partial `Homol` folders:
```
micmac-disttapioca-combine -i DistributedTapiocaAllOutputs -o Homol
```
Now we have a `Homol` folder that was created in a distributed manner. We can plot the combined CPU/MEM usage for all the nodes of the cluster:
```
coeman-mon-plot-cpu-mem -i DistributedTapiocaAllOutputs -r 20
```

#### Distributed dense image matching

In the previous subsection we ran Tapioca in a distributed system. After Tapioca we need to run Tapas (and maybe GCPBascule or other processes) in order to obtain the images orientation. We saw before that we can use tie-points reduction to speed-up Tapas. After we have th eimage orientation, we are ready to generate the dense colored point cloud. In MicMac this can be done with the dense image matching pipeline that consists of Malt, Tawny and Nuage2Ply. These processes are very time consuming and will generate a large amount of intermediate data that for large datasets will fill your disk storage easily.

We have developed a distributed tool to run the dense image matching pipeline (Malt, Tawny and Nuage2Ply). Right now the solution only works for aerial images oriented in a cartographic reference system. In this example we show how to run it in a SGE cluster. We assume that we have the data (images) again in `/var/scratch/orubi/data/medium/4ms_60m_1000` and in this folder we also have the image orientation in the folder `Ori-Final`.

In order to run the distributed dense image matching, first we need to divide the processing in chunks. The tool `micmac-distmatching-create-config` can be used to define the different chunks and the processing that needs to be done for each chunk:
```
micmac-distmatching-create-config -i TPROutput/Ori-GCPBOut -e JPG -o DistributedMatching.xml -f DistributedMatchingConfigFolder -n 60,60
```
The previous command divides the area in 3600 tiles. Which images are processed in each tile is defined in the `DistributedMatchingConfigFolder` folder. For each tile it defines the commands to execute and all the commands are stored in `DistributedMatching.xml`.

Now we use the tool `coeman-par-sge` in pycoeman to run the list of commands in the cluster and in parallel:
```
cd /var/scratch/orubi/data/medium/4ms_60m_1000
coeman-par-sge -d . -c DistributedMatching.xml -s /home/orubi/sw/export_paths.sh -r /local/orubi/DistributedMatching -o DistributedMatchingAllOutputs
```

`/var/scratch/orubi/data/medium/4ms_60m_1000` is our shared data location, so all paths in the XML files are relative to this location. The various commands to run in the cluster are specified in `DistributedMatching.xml`. The file `/home/orubi/sw/export_paths.sh` is a file that sets the environment in the nodes. Once a job is going to be executed in a certain node, the node needs to have the software available (MicMac, pymicmac and pycoeman). The execution of the jobs in the nodes will be done in the location specified, i.e. `/local/orubi/DistributedMatching`. For each job the required data for the tile will copied from the shared data location (`/var/scratch/orubi/data/medium/4ms_60m_1000`) to the local disk (`/local/orubi/DistributedMatching`) so each job has a local copy of the required data for faster access. The tile will be processed locally in the node and the output data (the pointlcoud of the tile) will be copied back to the shared location.

After the exectuion is finished, we have a `DistributedMatchingAllOutputs` folder that contains subfolders and each subfolder contains a ply file. We can plot the combined CPU/MEM usage for all the nodes of the cluster:
```
coeman-mon-plot-cpu-mem -i DistributedMatchingAllOutputs -r 20
```
