#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import subprocess

VERSION = '0.0.4'

README = open('README.md').read()

flags = subprocess.check_output(['pkg-config', '--cflags-only-I', 'opencv'])
include_dirs_list = [flag[2:] for flag in flags.split()]
include_dirs_list.append('.')
flags = subprocess.check_output(['pkg-config', '--libs-only-L', 'opencv'])
library_dirs_list = flags
flags = subprocess.check_output(['pkg-config', '--libs', 'opencv'])
libraries_list = []
for flag in flags.split():
    libraries_list.append(flag)

EXTENSIONS = [
        Extension(
                  "rh_renderer/blender/images_composer",
                  ["rh_renderer/blender/images_composer.pyx", "rh_renderer/blender/ImagesComposer.cpp",
                   "rh_renderer/blender/images_composer.pyx", "rh_renderer/blender/detail/seam_finders.cpp",
                   "rh_renderer/blender/images_composer.pyx", "rh_renderer/blender/detail/exposure_compensate.cpp",
                   "rh_renderer/blender/images_composer.pyx", "rh_renderer/blender/detail/blenders.cpp"],
                  language="c++",
                  include_dirs=include_dirs_list,
                  extra_compile_args=['-O3', '--verbose'],
                  extra_objects=libraries_list
                 )
]
setup(
    name='rh_renderer',
    version=VERSION,
    packages=find_packages(),
    ext_modules = cythonize(EXTENSIONS),
    author='Adi Suissa-Peleg',
    author_email='adisuis@seas.harvard.edu',
    url="https://github.com/Rhoana/rh_renderer",
    description="Rhoana's rendering library",
    long_description=README,
    include_package_data=True,
    install_requires=[
        "numpy>=1.9.3",
        "scipy>=0.16.0",
        "Cython>=0.23.3",
    ],
    dependency_links = ['http://github.com/Rhoana/tinyr/tarball/master#egg=tinyr-0.1'],
    zip_safe=False
)
