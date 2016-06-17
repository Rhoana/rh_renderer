#!/usr/bin/env python
import os
from setuptools import setup, find_packages

VERSION = '0.0.2'

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
    dependency_links = ['http://github.com/Rhoana/pyrtree/tarball/master#egg=pyrtree-0.5'],
    zip_safe=False
)
