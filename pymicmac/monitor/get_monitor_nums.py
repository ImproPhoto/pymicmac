 #!/usr/bin/python
import sys, numpy, os, argparse, pandas
from tabulate import tabulate
from pymicmac import utils_execution

def readFile(fileName, resampling = None, ignoreLargeJumps = False):
    lines = open(fileName, 'r').read().split('\n')
    numlines = len(lines)

    hostname = None
    numcores = None
    memtotal = None
    if lines[0].startswith('#Host name:'):
        hostname = lines[0].split(':')[-1]
    else:
        raise Exception('First line in .mon file must include #Host name:')
    if lines[1].startswith('#Number cores:'):
        numcores = int(lines[1].split(':')[-1])
    else:
        raise Exception('Second line in .mon file must include #Number cores:')
    if lines[2].startswith('#System memory [GB]:'):
        memtotal = float(lines[2].split(':')[-1])
    else:
        raise Exception('Third line in .mon file must include #System memory [GB]:')

    t = []
    d = []
    for i in range(numlines):
        line = lines[i]
        if not line.startswith('#'):
            fields = lines[i].split()
            if len(fields) == 3:
                t.append(float(fields[0]))
                d.append((float(fields[1]),float(fields[2])))

    if ignoreLargeJumps:
        t = numpy.array(t)
        diff = t[1:] - t[:-1]
        tn = []
        tn.append(t[0])
        acc = 0.
        for i in range(1,len(t)):
            if diff[i-1] > 5.:
                acc+=diff[i-1]
            tn.append(t[i] - acc)
        t = tn

    df = pandas.DataFrame(data=numpy.array(d),index=t,columns=['CPU','MEM'])
    df.index = pandas.to_datetime(df.index, unit='s')
    df = df.groupby(df.index).first()
    df.index.rename('Time')
    df['MEM'] = ((df['MEM'] / 100.) * memtotal)
    if resampling != None:
        df = df.resample(str(resampling) + 's')
    return (df, hostname, numcores, memtotal)

def run(tools, folders, ignoreLargeJumps):

    tools = tools.split(',')
    folders = folders.split(',')

    table = []
    header = ['#Tool', 'Name', 'Time[s]', 'Avail. CPU', 'Max. CPU', 'Mean CPU', 'Avail. MEM[GB]', 'Max. MEM[GB]', 'Mean MEM[GB]']

    for tool in tools:
        for folder in folders:
            monFileNanme = folder + '/' + tool + '.mon'
            if os.path.isfile(monFileNanme):
                (df, hostname, numcores, memtotal)  = readFile(monFileNanme, ignoreLargeJumps=ignoreLargeJumps)
                pattern = "%0.2f"
                table.append([tool, folder, pattern % (df.index[-1] - df.index[0]).total_seconds(), pattern % (numcores * 100.), pattern % df['CPU'].max(), pattern % df['CPU'].mean(), pattern % memtotal, pattern % df['MEM'].max(), pattern % df['MEM'].mean()])
            else:
                table.append([tool, folder] + ['-'] * (len(header) - 2))

    print("##########################")
    print("Time/CPU/MEM tools monitor")
    print("##########################")
    print(tabulate(table, headers=header))
    print()


def argument_parser():
   # define argument menu
    description = "Get elapsed time and CPU/MEM stats for MicMac tools executed using pymicmac."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-t', '--tools',default='', help='Comma-separated list of tools (it is expected that in each execution folder there is a <tool name>.mon for each specified tool)', type=str, required=True)
    parser.add_argument('-f', '--folders',default='', help='Comma-separated list of execution folders where to look for the .mon files', type=str, required=True)
    parser.add_argument('--ignoreLargeJumps', default=False, help='If enabled, it ignores large (> 5 seconds) time jumps in the monitor files. Use this for example when you were running your processes in a Virtual Machine and you had to suspend it for a while [default is disabled]', action='store_true')
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.tools, a.folders, a.ignoreLargeJumps)
    except Exception as e:
        print(e)
