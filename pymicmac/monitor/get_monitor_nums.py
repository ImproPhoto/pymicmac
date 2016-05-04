 #!/usr/bin/python
import sys, numpy, os
from tabulate import tabulate

tools = sys.argv[1].split(',')
folders = sys.argv[2:len(sys.argv)]

table = []
header = ['#Tool', 'Name', 'Time[s]', 'MaxCPU', 'MeanCPU', 'MaxMEM', 'MeanMEM']

for tool in tools:
    for folder in folders:
        monFileNanme = folder + '/' + tool + '.mon'

        if os.path.isfile(monFileNanme):
            lines = open(monFileNanme,'r').read().split('\n')

            t = []
            c = []
            m = []

            for line in lines:
                fields = line.split()
                if len(fields) == 3:
                    t.append(float(fields[0]))
                    c.append(float(fields[1]))
                    m.append(float(fields[2]))

            pattern = "%0.2f"
            table.append([tool, folder, pattern % t[-1], pattern % numpy.max(c), pattern % numpy.mean(c), pattern % numpy.max(m), pattern % numpy.mean(m)])
        else:
            table.append([tool, folder, '-', '-', '-', '-', '-'])

print("##########################")
print("Time/CPU/MEM tools monitor")
print("##########################")
print(tabulate(table, headers=header))
print()
