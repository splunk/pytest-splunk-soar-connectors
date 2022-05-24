#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import setuptools

def read(*args):
    file_path = pathlib.Path(__file__).parent.joinpath(*args)
    with file_path.open(encoding="utf-8") as f:
        return f.read()

setuptools.setup(
    name='pytest-splunk-soar-connectors',
    version='0.1.0',
    author='Daniel Federschmidt',
    author_email='dfederschmidt@splunk.com',
    maintainer='Daniel Federschmidt',
    maintainer_email='dfederschmidt@splunk.com',
    license='Apache Software License 2.0',
    url='https://github.com/dfederschmidt/pytest-splunk-soar-connectors',
    description='A simple plugin to use with pytest',
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=['pytest_splunk_soar_connectors', 'phantom_mock'],
    python_requires='>=3.5',
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=['pytest>=3.5.0', 'rich'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'splunk-soar-connectors = pytest_splunk_soar_connectors',
        ],
    },
)
