#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='repl',
    version='1.0',
    description='Run command as REPL-environment (useful for git!).',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='https://github.com/mbr/repl',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'repl = repl.cli:repl',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ])
