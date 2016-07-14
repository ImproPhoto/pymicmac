 #!/usr/bin/python
import sys, os, math, glob, argparse
import numpy
import matplotlib.pyplot as plt
from pymicmac import utils_execution
from pymicmac.monitor import get_monitor_nums

def run(inputArgument, resampling, ignoreLargeJumps):
    availMap = {}
    if os.path.isfile(inputArgument):
        (df, hostname, numcores, memtotal)  = get_monitor_nums.readFile(inputArgument, resampling, ignoreLargeJumps)
        availMap[hostname] = (numcores, memtotal)
    else:
        if resampling == None or resampling < 5:
            raise Exception('Resampling must be higher than 5 if combining monitor files!')

        monFiles = glob.glob(inputArgument + '/*.mon')
        df_inter_sum = None
        for i in range(len(monFiles)):
            (df, hostname, numcores, memtotal)  = get_monitor_nums.readFile(monFiles[i], resampling, ignoreLargeJumps)
            availMap[hostname] = (numcores, memtotal)
            df_inter = df.interpolate(method='time')
            if i == 0:
                df_inter_sum = df_inter
            else:
                df_inter_sum = df_inter_sum.add(df_inter, fill_value=0)
        df = df_inter_sum

    print('Elapsed time: ' + str((df.index[-1] - df.index[0]).total_seconds()))
    print('Avg. CPU: ' + '%0.2f' % df['CPU'].mean())
    print('Avg. MEM [GB]: ' + '%0.2f' % df['MEM'].mean())
    print('Numger used hosts: ' + str(len(availMap)))
    (availCPU, availMEM) = numpy.array(list(availMap.values())).sum(axis=0)
    print('Avail. CPU: ' + '%0.2f' % (100. * availCPU))
    print('Avail. MEM [GB]: ' + '%0.2f' % availMEM)

    fig, ax1 = plt.subplots()
    df['CPU'].plot(ax=ax1)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('CPU [%]', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax2 = ax1.twinx()
    df['MEM'].plot(ax=ax2, color='r')
    ax2.set_ylabel('MEM [GB]', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.show()

def argument_parser():
   # define argument menu
    description = "Plot the CPU/MEM usage of a tool executed pymicmac (it is possible to combine .mon file of a tool executed in distributed manner)"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input',default='', help='Input argument. It can be a single .mon file or a folder full of .mon files. In the case of a folder, the .mon files are resampled/interpolated/combined to displaya single graph with the aggregated CPU/MEM usage', type=str, required=True)
    parser.add_argument('-r', '--resampling',default=None, help='Resampling of the time series (it input is a folder, resampling must be higher than 5)', type=int, required=False)
    parser.add_argument('--ignoreLargeJumps', default=False, help='If enabled, it ignores large (> 5 seconds) time jumps in the monitor files. Use this for example when you were running your processes in a Virtual Machine and you had to suspend it for a while [default is disabled]', action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.input, a.resampling, a.ignoreLargeJumps)
    except Exception as e:
        print(e)
