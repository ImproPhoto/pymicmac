 #!/usr/bin/python
 import sys,os
from tabulate import tabulate

header = ['#Name', 'CInit', 'Ini', 'CEnd', 'End']
table = []
for i in range(1,len(sys.argv)):
    folderName = sys.argv[i]
    if folderName.endswith('/'):
        folderName = folderName[:-1]
    logFileName = folderName + '/RedTieP.log'
    logFolderName = folderName + '/RedTieP_logs'
    if os.path.isdir(logFolderName):
        lines = os.popen('cat ' + logFolderName + '/*').read().split('\n')
    elif os.path.isfile(logFileName):
        lines = open(logFileName, 'r').read().split('\n')
    inits = []
    ends = []
    c1 = 0
    c2 = 0
    for line in lines:
        if line.count('#InitialHomolPoints:'):
            c1+=1
            inits.append(int(line.split(' ')[0].split(':')[-1].replace('.','')))
        if line.count('#HomolPoints:'):
            c2+=1
            ends.append(int(line.split(' ')[1].split('=>')[-1].split('(')[0]))

    table.append([folderName, str(c1), str(sum(inits)), str(c2), str(sum(ends))])

print("#################")
print("RedTieP reduction")
print("#################")
print(tabulate(table, headers=header))
