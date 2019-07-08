#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slacks",
    version="0.0.1",
    author="Wojciech Puchta, Hicron DSS",
    author_email="wojciech.puchta@hicron.com",
    description="CLI utility for slack notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hicdss/slacks",
    packages=setuptools.find_packages(),
    scripts=['bin/slacks'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)