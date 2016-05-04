 #!/usr/bin/python
import sys
import matplotlib.pyplot as plt

inputArgument = sys.argv[1]

lines = open(inputArgument, 'r').read().split('\n')

t = []
tots = []
useds = []

for line in lines:
    fields = line.split()
    if len(fields) == 4:
        t.append(float(fields[0]))
        tots.append(int(fields[1]) / 1048576)
        useds.append(int(fields[2]) / 1048576)

l1, = plt.plot(t, tots, 'r--')
l2, = plt.plot(t, useds, 'b.-')

plt.legend((l1, l2), ('Total Disk', 'Used Disk'), loc='upper right', shadow=True)
plt.xlabel('Time [s]')
plt.ylabel('Disk [MB]')
#plt.title('Damped oscillation')
plt.show()
