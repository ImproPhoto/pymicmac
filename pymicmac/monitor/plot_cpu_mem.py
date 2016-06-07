 #!/usr/bin/python
import sys, os, math, glob
import numpy
import matplotlib.pyplot as plt

def readFile(fileName, ignoreLargeJumps):
    lines = open(fileName, 'r').read().split('\n')
    t = []
    c = []
    m = []
    for line in lines:
        fields = line.split()
        if len(fields) == 3:
            t.append(float(fields[0]))
            c.append(float(fields[1]))
            m.append(float(fields[2]))
    if ignoreLargeJumps:
        t = numpy.array(t)
        d = t[1:] - t[:-1]
        tn = []
        tn.append(t[0])
        acc = 0.
        for i in range(1,len(t)):
            if d[i-1] > 5.:
                acc+=d[i-1]
            tn.append(t[i] - acc)
        t = tn
    return (t,c,m)

inputArgument = sys.argv[1]

if os.path.isfile(inputArgument):
    (t,c,m) = readFile(inputArgument, len(sys.argv) == 3 and sys.argv[2] == 'True')
    print('Elapsed time: ' + str(t[-1]))

else:

    nodeMem = int(sys.argv[2])

    monFiles = glob.glob(inputArgument + '/*.mon')
    monFilesData = []

    minTIni = None
    maxTEnd = None

    for i in range(len(monFiles)):
        monFile = monFiles[i]
        (t,c,m) = readFile(monFile, len(sys.argv) == 3 and sys.argv[2] == 'True')
        tLMFile = os.path.getmtime(monFile)
        if maxTEnd == None or maxTEnd < tLMFile:
            maxTEnd = tLMFile
        tIniFile = tLMFile - t[-1]
        t = numpy.array(t) + tIniFile
        if minTIni == None or minTIni > tIniFile:
            minTIni = tIniFile

        monFilesData.append((t,c,m))

    tElapsedTotal = maxTEnd - minTIni
    print('Elapsed time total: ' + str(tElapsedTotal))

    t = range(int(math.ceil(tElapsedTotal)))
    c = []
    m = []
    for i in range(len(t)):
        c.append(0)
        m.append(0)

    for i in range(len(monFilesData)):
        (tm, cm, mm) = monFilesData[i]
        for j in range(len(tm)):
            ii = int(math.floor(tm[j] - minTIni))
            c[ii] += cm[j]
            m[ii] += ((mm[j] / 100.) * nodeMem)



print('Avg. CPU: ' + str(numpy.array(c).mean()))
print('Avg. MEM: ' + str(numpy.array(m).mean()))

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
