"""This is a module for PiPlus from SunFounder.

See:
https://www.sunfounder.com
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
import ds1307setup as DS1307

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PiPlus',
    version='1.0.0',
    description='PiPlus python module for Raspberry Pi',
    long_description=long_description,

    url='https://www.sunfounder.com',

    author='Cavon Lee',
    author_email='lijiarong@sunfounder.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='Raspberry Pi',

    packages=find_packages(exclude=['example', 'docs', 'tests*']),

    install_requires=['RPi.GPIO'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={
        'PiPlus': ['package_data.dat'],
    },
    data_files=[('data', ['data/data_file'])],

    entry_points={
        'console_scripts': [
            'PiPlus=PiPlus:main',
        ],
    },
)
	
DS1307.setup()
