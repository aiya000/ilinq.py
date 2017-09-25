#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from ilinq import __VERSION__

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]

setup(
    name='ilinq',
    version=__VERSION__,
    description='linq library',
    author='yassu',
    author_email='yasu0320.dev@gmail.com',
    classifiers=classifiers,
    url='https://github.com/yassu/ilinq.py',
  )
