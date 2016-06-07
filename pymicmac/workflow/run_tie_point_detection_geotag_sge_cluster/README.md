# Run Tapioca in a SGE cluster

This scripts can be used to run `Tapioca File` in a cluster with Grid Engine (SGE) batch queueing system.

## Instructions

- Install pymicmac if you have not done it before

- Copy the 3 files in this folder to your working directory in a shared folder in the cluster (your home directory or a shared disk between all cluster nodes).

- Use the `xmlmm/split_tapioca_filelist.py` to split the XML file used by `Tapioca File` in multiple ones:

```python [path to pymicmac]/pymicmac/xmlmm/split_tapioca_filelist.py -i [input XML] -o [folder for output XMLs] -n [number of image pairs per output XML, must be even number]```

Depending in the maximum job execution time of the cluster you are using, chose a number wisely. For example, we chose 20 to have jobs that last less than 10 minutes.

- Use the `generate_jobs.py` to generate the list of SGE jobs (qsubs instructionsi, one for each XML generated in the previous step):

```python generate_jobs.py [folder with XMLs] [Set environment file] [Shared folder] [Local working folder] > run_all.sh``` 

Where:
   -- `[Set environment file]` is a file that will be sourced before the execution of Tapioca in each job executed in the nodes. The file must contain instruction to set the environment in the nodes (namely to make micmac, its requirements and pymicmac available in PATH and PYTHONPATH)
   -- `[Shared folder]` is a folder shared by all the nodes in the cluster where the images to process are contained
   -- `[Local working folder]` is the folder that will be used in each job execution in the cluster nodes. Obviously, the folder has to be a valid one in the nodes

This will generate the list of jobs in a `run_all.sh`. 

-- Run `chmod a+x run_all.sh` to make it executable and then execute it to submit the jobs to the queue. For each job a folder `Homol_[id]` will be created inside `[Shared folder]/MultiHomol`. The `Homol_[id]` contains the results of Tapioca for a job.

-- After all jobs have finished you will have a `MultiHomol` folder in the the `[Shared folder]` with all the partial results that need joining. Use `pymicmac/other/join_homol.py` to join them into a final Homol folder 

```python [path to pymicmac]/pymicmac/other/join_homol.py -i [MultiHomol path] -o [output Homol folder]```
