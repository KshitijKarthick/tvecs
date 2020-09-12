#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""Setuptools Module."""

import os

from setuptools import setup, find_packages


def read(fname):
    """"Utility function to read README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='tvecs',
    version='1.0',
    url='https://github.com/kshitijkarthick/t-vecs',
    license='MIT',
    author="Kshitij Karthick, Ravi Kumar L, Prarthana Sannamani, Prateeksha",
    author_email='https://github.com/kshitijkarthick/t-vecs/issues',
    description='Map words across different semantic vector spaces',
    long_description=read('README.rst'),
    packages=find_packages(),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md']
    },
    include_package_data=True,
    keywords="word2vec semantic similarity vector space mapping",
    zip_safe=False,
    platforms='any',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'numpy==1.19.2',
        'CherryPy==18.6.0',
        'gensim==3.8.3',
        'Jinja2',
        'nltk==3.5',
        'scipy==1.5.2',
        'regex',
        'scikit-learn == 0.23.2',
        'html5lib',
        'beautifulsoup4',
        'PyDictionary',
    ],
    use_2to3=True,
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Framework :: Sphinx',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Documentation :: Sphinx'
    ],
    entry_points={
        'console_scripts': [
            'tvecs = tvecs.__main__:args_parser',
        ],
        'setuptools.installation': [
            'eggsecutable = tvecs.__main__:args_parser',
        ]
    }
)
