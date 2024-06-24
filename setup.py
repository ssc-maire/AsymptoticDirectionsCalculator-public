from setuptools import find_packages, setup
import os
import glob as gb

# get requirements for installation
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='AsympDirsCalculator',
    packages=find_packages(exclude='tests'),
    package_data={"AsympDirsCalculator":["magcos_running_scripts/runNoRewriteMAGCOSsimulation.sh",
                                         "magcos_running_scripts/AsymptoticDirection.g4mac",
                                         ]},
    version='1.0.11',
    description='Python library containing tools for calculating asymptotic directions and vertical cut-off rigidities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Space Environment and Protection Group, University of Surrey',
    url='https://github.com/ssc-maire/AsymptoticDirectionsCalculator-public',
    keywords = 'space physics earth asymptotic trajectory geomagnetic rigidity magnetocosmics',
    license='GNU General Public License v3.0',
    install_requires= ['numpy>=1.21.6',
                        'pandas>=1.3.5',
                        'setuptools>=45.2.0',
                        'tqdm>=4.30.0',
                        'joblib>=1.2.0',
                        'wheel>=0.38.4'],
    #install_requires,
    setup_requires=['pytest-runner','wheel'],
    tests_require=['pytest'],
)
