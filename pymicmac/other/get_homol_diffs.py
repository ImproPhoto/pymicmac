 #!/usr/bin/python
import sys, numpy
from tabulate import tabulate
from pymicmac import utils_execution

table = []
header = ['#Name', 'RedHomol/Homol']

rootHomolSize = utils_execution.getSize('Homol')

for i in range(1,len(sys.argv)):
    folderName = sys.argv[i]
    homolSize = utils_execution.getSize(folderName + '/Homol' )
    pattern = "%0.4f"
    if homolSize > 0:
        table.append([folderName, pattern % ((homolSize/rootHomolSize))])
    else:
        table.append([folderName, '-'])

print("#####################")
print("Ratio Homol reduction")
print("#####################")
print(tabulate(table, headers=header))
print()
