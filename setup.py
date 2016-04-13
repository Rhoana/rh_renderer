#!/usr/bin/env python
import os

from setuptools import setup, find_packages

VERSION = 0.0.1
version = os.path.join('rh_renderer', '__init__.py')
execfile(version)

README = open('README.md').read()

setup(
    name='rh_renderer',
    version=VERSION,
    packages=find_packages(),
    author='Adi Suissa-Peleg',
    author_email='adisuis@seas.harvard.edu',
    url="https://github.com/Rhoana/rh_renderer",
    description="Rhoana's rendering library",
    long_description=README,
    include_package_data=True,
    install_requires=[
        "numpy>=1.9.3",
        "scipy>=0.16.0",
    ],
    zip_safe=False
)
