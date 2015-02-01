from __future__ import print_function
from setuptools import setup, find_packages
import io
#import codecs
import os
#import sys

import dbnormalizer

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')




setup(
    name='dbnormalizer',
    version=dbnormalizer.__version__,
    url='https://github.com/mairaladeira/adb_project',
    install_requires=[
                      'SQLAlchemy>=0.8.2',
                      'flask>=0.10.1',
                      'psycopg2>=2.5.4',
                    ],
    description='Database Normalizer for the Advanced Databases Course of DMKM master',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: ADB course',
        'Operating System :: OS Independent',
        ],
    extras_require={
    }
)
