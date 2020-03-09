#!/usr/bin/env python3

"""Setup script"""

from setuptools import setup, find_packages

setup(
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['test']),
    use_scm_version=True,
    python_requires='>=3.7',
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=([
        'python-dateutil',
        'pyyaml',
        'requests',
    ]),
    test_suite='test',
)
