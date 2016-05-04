 #!/usr/bin/python
import sys
import matplotlib.pyplot as plt

inputArgument = sys.argv[1]

lines = open(inputArgument, 'r').read().split('\n')

t = []
c = []
m = []

for line in lines:
    fields = line.split()
    if len(fields) == 3:
        t.append(float(fields[0]))
        c.append(float(fields[1]))
        m.append(float(fields[2]))

fig, ax1 = plt.subplots()
ax1.plot(t, c, 'b.-')
ax1.set_xlabel('Time [s]')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('CPU [%]', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')

ax2 = ax1.twinx()
ax2.plot(t, m, 'r.-')
ax2.set_ylabel('MEM [%]', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')

plt.show()
