#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:09:15 2020

@author: vector
"""
import sys
import os
from setuptools import setup
from ismartcsv.version import __version__

with open('README.md','r') as fh:
    long_description = fh.read()


packages=['ismartcsv',]

#setup automatic publishing to pypi, use $python setup.py publish
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

#to build the package, use $python setup.py build
if sys.argv[-1] == 'build':
    os.system('python setup.py sdist bdist_wheel')
    sys.exit()



setup(
    name="ismartcsv",
    version=__version__,
    author="jeldikk",
    author_email="jeldi.kamal2013@gmail.com",
    description="ismartcsv - smart way to handle scientific instrument generated csv files",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jeldikk/ismartcsv",
    packages = packages,
    install_requires=['numpy', 'matplotlib', 'pyYAML'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6"

)