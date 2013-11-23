#!/usr/bin/env python

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

setup(
    name='crypto-trade',
    version='0.0.1',
    description='Interface to the API at www.crypto-trade.com',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='bitcoin altcoin namecoin litecoin',
    packages=find_packages(),
)
