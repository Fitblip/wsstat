from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

import wsstat

py_version = sys.version_info[:2]

if py_version < (3, 3):
    raise Exception("websockets requires Python >= 3.3.")

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

long_description = """
WSStat is a tool for stress testing and monitoring the health of websocket servers/connections.

You can find a demo at https://cloud.githubusercontent.com/assets/1072598/18814490/bb2fb2b0-82c9-11e6-8a35-6b80c0f40dc3.gif, and the project itself at https://github.com/Fitblip/wsstat.

As of right now this tool is still a bit rough around the edges, but stable enough for a v1.
"""

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
            'wsstat = wsstat.main:wsstat_console',
        ],
    },
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
        "Environment :: Console",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    extras_require={
        'testing': ['pytest'],
    },

)
