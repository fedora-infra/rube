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
        return f.read()


def get_requirements(fname='requirements.txt'):
    with open(fname, 'r') as f:
        return f.readlines()

setup(
    name='rube.fedora',
    version='0.1.0',
    description="Rube tests for Fedora Infrastructure",
    long_description=get_description(),
    install_requires=get_requirements(),
    test_suite='nose.collector',
    url="http://github.com/fedora-infra/rube/",
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    license='AGPL',
    packages=['rube', 'rube.fedora'],
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
