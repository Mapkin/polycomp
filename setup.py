#!/usr/bin/env python
from __future__ import print_function

import errno
import os
import subprocess

from distutils.errors import DistutilsPlatformError
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


class build_ext_with_cython(build_ext):
    def generate_c_file(self):
        try:
            if (os.path.exists("polycomp/speedups.c") and
                os.path.getmtime("polycomp/speedups.pyx") < os.path.getmtime("polycomp/speedups.c")):
                print("polycomp/speedups.c up to date.")
                return
            print("creating polycomp/speedups.c")
            proc = subprocess.Popen(["cython", "polycomp/speedups.pyx"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        except OSError as e:
            if e.errno == errno.ENOENT:
                print("Couldn't find cython command.")
                raise DistutilsPlatformError("Failed to generate C file with Cython.")
            else:
                raise
        out = proc.communicate()[0]
        result = proc.wait()
        if result != 0:
            print("Error during C file generation with Cython:")
            print(out)
            raise DistutilsPlatformError("Failed to generate C file with Cython.")

    def run(self):
        try:
            self.generate_c_file()
        except DistutilsPlatformError:
            if os.path.exists("polycomp/speedups.c"):
                print("Found existing C file, ignoring errors.")
            else:
                raise
        build_ext.run(self)


ext_modules = [
    Extension("polycomp.speedups", ["polycomp/speedups.c"]),
]


setup(
    name = "polycomp",
    version = "1.1.0",
    author = "Mapkin",
    author_email = "opensource@mapkin.co",
    url = "https://github.com/Mapkin/polycomp",
    license="MIT License",
    description = "Polyline compression package.",
    long_description=open("README.md").read(),
    packages = find_packages(),
    ext_modules = ext_modules,
    extras_require={
        'test': ['pytest'],
    },
    cmdclass = {'build_ext': build_ext_with_cython},
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)
