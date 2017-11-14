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

# Third we see if pycoeman has been manually installed and is in PYTHONPATH
try:
    import pycoeman
except:
    print('Installation could not be done: pycoeman could not be found.')
    sys.exit(1)

setup(
    name='pymicmac',
    version='1.0.0',
    packages=['pymicmac', 'pymicmac.logsparser', 'pymicmac.logsplotter', 'pymicmac.noodles', 'pymicmac.workflow', 'pymicmac.workflow.distributed_tapioca', 'pymicmac.workflow.distributed_matching',],
    license='',
    long_description=open('README.md').read(),
    author='Oscar Martinez-Rubi',
    author_email='o.rubi@esciencecenter.nl',
    url='https://github.com/ImproPhoto/pymicmac',
    install_requires=[
          'numpy', 'tabulate', 'matplotlib', 'lxml', 'noodles==0.2.4', 'pycoeman', 'scipy'
    ],
    entry_points={
        'console_scripts': [
            'micmac-run-workflow=pymicmac.workflow.run_workflow:main',
            'micmac-disttapioca-create-pairs=pymicmac.workflow.distributed_tapioca.create_all_image_pairs_file:main',
            'micmac-disttapioca-create-config=pymicmac.workflow.distributed_tapioca.create_parcommands_config_file:main',
            'micmac-disttapioca-combine=pymicmac.workflow.distributed_tapioca.combine_distributed_tapioca_output:main',
            'micmac-distmatching-create-config=pymicmac.workflow.distributed_matching.create_parcommands_config_file:main',
            'micmac-tapas-log-anal=pymicmac.logsparser.get_tapas_nums:main',
            'micmac-redtiep-log-anal=pymicmac.logsparser.get_redtiep_nums:main',
            'micmac-campari-log-anal=pymicmac.logsparser.get_campari_nums:main',
            'micmac-gcpbascule-log-anal=pymicmac.logsparser.get_gcpbascule_nums:main',
            'micmac-homol-compare=pymicmac.logsparser.get_homol_diffs:main',
            'micmac-gcpbascule-log-plot=pymicmac.logsplotter.plot_gcpbascule_nums:main',
            'micmac-campari-log-plot=pymicmac.logsplotter.plot_campari_nums:main',
            'micmac-gcps-plot=pymicmac.logsplotter.plot_gcps:main',
            'micmac-tiep-plot=pymicmac.logsplotter.plot_tiep:main',
            'micmac-noodles=pymicmac.noodles.noodles_exe_parallel:main',
        ],
    },
)
