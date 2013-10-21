# -*- coding: utf-8 -*-
# This file is part of Rube.
#
# Rube is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rube is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Rube.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os

from setuptools import setup

# Ridiculous as it may seem, we need to import multiprocessing and logging here
# in order to get tests to pass smoothly on python 2.7.
try:
    import multiprocessing
    import logging
except:
    pass


def get_description(fname='README.rst'):
    with open(fname, 'r') as f:
        return f.read().split('.. split here\n')[1]


def get_requirements(fname='requirements.txt'):
    with open(fname, 'r') as f:
        return f.readlines()


setup(
    name='rube.core',
    version='0.1.2',
    description="A convenience layer on top of selenium",
    long_description=get_description(),
    install_requires=get_requirements(),
    test_suite='nose.collector',
    url="http://github.com/fedora-infra/rube/",
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    license='GPLv3+',
    packages=['rube', 'rube.core'],
    namespace_packages=['rube'],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
