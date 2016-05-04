 #!/usr/bin/python
import sys, os
from tabulate import tabulate

table = []
header = ['#Name', 'CRes', 'Res', 'CWor', 'Wor']

for i in range(1,len(sys.argv)):
    folderName = sys.argv[i]
    if folderName.endswith('/'):
        folderName = folderName[:-1]
    logFileName = folderName + '/Tapas.log'
    if os.path.isfile(logFileName):
        lines = open(logFileName, 'r').read().split('\n')
        residuals = []
        worsts = []
        c1 = 0
        c2 = 0
        for line in lines:
          if line.count('Residual = '):
              c1+=1
              residuals.append(line.split(';;')[0].replace('| |  Residual = ',''))
          elif line.count(' Worst, Res '):
              c2+=1
              worsts.append(line.split('for')[0].replace('| |  Worst, Res ',''))
        if len(worsts) and len(residuals):
            table.append([folderName, str(c1), residuals[-1], str(c2), worsts[-1]])
        else:
            table.append([folderName, '-', '-', '-', '-'])
    else:
        table.append([folderName, '-', '-', '-', '-'])

print("##########################")
print("Tapas last residuals/worts")
print("##########################")
print(tabulate(table, headers=header))
print()
