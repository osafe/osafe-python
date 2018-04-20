#!/usr/bin/env python3

from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="osafe",
    version="1.0.0",
    description="",
    license="MIT",
    url="https://github.com/osafe/osafe-python",
    author="Oded Niv",
    author_email="oded.niv@gmail.com",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ]
)
