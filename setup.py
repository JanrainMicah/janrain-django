#!/usr/bin/env python
import distribute_setup
distribute_setup.use_setuptools()

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from janrain.django import get_version

setup(
    name = "janrain-django",
    version = get_version(),
    description = "Janrain integration with Django",
    long_description = read("README.rst"),
    author = "Micah Carrick",
    author_email = "micah@janrain.com",
    url = "http://developers.janrain.com/",
    packages = find_packages(),
    namespace_packages = ["janrain"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License"
    ],
    #test_suite = "janrain.django.test"
    install_requires = [
        'janrain-python-api >= 0.2.1',
    ],
)
