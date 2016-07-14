from distutils.core import setup
import subprocess, sys

# First we check MicMac in installed and in the PATH
(out,err) = subprocess.Popen('mm3d -help', shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
if out.decode(sys.stdout.encoding).count('MicMac') == 0:
    print('Installation could not be done: MicMac (mm3d) could not be found.')
    sys.exit(1)

# Second we see if noodles has been manually installed and is in PYTHONPATH
try:
    import noodles
except:
    print('Installation could not be done: noodles could not be found.')
    sys.exit(1)

setup(
    name='pymicmac',
    version='0.1dev',
    packages=['pymicmac', 'pymicmac.logsparser', 'pymicmac.logsplotter', 'pymicmac.monitor', 'pymicmac.noodles', 'pymicmac.other', 'pymicmac.workflow', 'pymicmac.xmlmm'],
    license='',
    long_description=open('README.md').read(),
    author='Oscar Martinez-Rubi',
    author_email='o.rubi@esciencecenter.nl',
    url='https://github.com/pymicmac/pymicmac',
    install_requires=[
          'numpy', 'tabulate', 'matplotlib', 'lxml', 'noodles'
    ],
)
