from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os
import sys

import wsstat

py_version = sys.version_info[:2]

if py_version < (3, 3):
    raise Exception("websockets requires Python >= 3.3.")

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='wsstat',
    version=wsstat.__version__,
    url='http://github.com/fitblip/wsstat/',
    author='Ryan Sears',
    tests_require=['pytest'],
    install_requires=dependencies,
    cmdclass={'test': PyTest},
    author_email='fitblip@gmail.com',
    description='Websocket health monitoring made simple (and beautiful)',
    long_description=long_description,
    packages=['wsstat'],
    include_package_data=True,
    test_suite='test.test_wsstat',
    entry_points={
        'console_scripts': [
            'wsstat = wsstat.main:run',
        ],
    },
    classifiers = [],
    extras_require={
        'testing': ['pytest'],
    }
)
