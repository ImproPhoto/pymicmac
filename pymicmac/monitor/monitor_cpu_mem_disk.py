#!/usr/bin/env python
import subprocess,sys,time,multiprocessing,os

def executeScript(osExeCommand, logFile):
    sys.stdout = open(logFile,'w')
    sys.stderr = sys.stdout
    subprocess.Popen(osExeCommand, shell = True, stdout=sys.stdout, stderr=sys.stdout).communicate()

def disk_usage(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return (total, used, free)

def getHostName():
    return os.popen('hostname').read().strip()

def getNumCores():
    return int(os.popen('nproc').read())

def getTotalMemGB():
    return int(os.popen('free -b').read().split('\n')[1].split()[1]) / 1073741824

def run(osExeCommand, logFile, monitorFile, diskMountPoint):
    o = open(monitorFile,'w')
    o2 = open(monitorFile + '.disk','w')

    o.write('#Host name: ' + str(getHostName()) + '\n')
    o.write('#Number cores: ' + str(getNumCores()) + '\n')
    o.write('#System memory [GB]: ' + str(getTotalMemGB()) + '\n')

    child = multiprocessing.Process(target=executeScript, args=(osExeCommand,logFile))
    child.start()

    counter = 0
    while child.is_alive():
        ti = time.time()
        command = 'top -b -n 1 | grep mm3d'
        (out,err) = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        lines = out.decode("utf-8").split("\n")
        c = 0
        m = 0
        for line in lines:
            if line != '':
                f = line.split()
                c+=float(f[8])
                m+=float(f[9])
        if (counter % 50) == 0:
            (total, used, free) = disk_usage(diskMountPoint)
            o2.write(("%0.2f" % ti) + ' ' + str(total) + ' ' + str(used) + ' ' + str(free) + '\n')
            o2.flush()
        o.write(("%0.2f" % ti) + ' ' + ("%0.2f" % c) + ' ' + ("%0.2f" % m) + '\n')
        o.flush()
        child.join(1)
        counter+=1
    o.close()
    o2.close()

if __name__ == "__main__":
    osExeCommand = sys.argv[1]
    monitorFile = sys.argv[2]
    diskMountPoint = sys.argv[3]
    run(osExeCommand, monitorFile, diskMountPoint)
