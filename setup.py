from distutils.core import setup

setup(
    name='PyMicMac',
    version='0.1dev',
    packages=['pymicmac',],
    license='',
    long_description=open('README.md').read(),
    author='Oscar Martinez-Rubi',
    author_email='o.rubi@esciencecenter.nl',
    url='https://github.com/pymicmac/pymicmac',
    install_requires=[
          'numpy', 'tabulate', 'matplotlib',
    ],
)
