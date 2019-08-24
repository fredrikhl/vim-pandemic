#!/usr/bin/env python
# encoding: utf-8
from distutils.core import setup

setup(
    name="Pandemic",
    version="1.2.0",
    author="http://jwcxz.com/",
    url="http://jwcxz.com/projects/vim-pandemic",
    requires=["argparse"],
    packages=["Pandemic"],
    scripts=["bin/pandemic"]
)
