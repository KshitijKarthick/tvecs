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
        'gensim==0.12.4',
        'nltk==3.1',
        'regex==2016.3.2',
        'scipy==0.17.1',
        'scikit-learn==0.15.2',
        'beautifulsoup4==4.4.1',
        'pytest==2.9.1',
        'html5lib==0.9999999'
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
