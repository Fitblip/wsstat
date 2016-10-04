# WSStat: Websocket stress testing made beautiful

[![Build Status](https://travis-ci.org/Fitblip/wsstat.svg?branch=master)](https://travis-ci.org/Fitblip/wsstat)
[![Coverage Status](https://coveralls.io/repos/github/Fitblip/wsstat/badge.svg?branch=master)](https://coveralls.io/github/Fitblip/wsstat?branch=master)
[![PyPi](https://img.shields.io/pypi/dm/wsstat.svg)](https://pypi.python.org/pypi/wsstat/)
[![PyPi](https://img.shields.io/pypi/v/wsstat.svg)](https://pypi.python.org/pypi/wsstat/)
[![PyPi](https://img.shields.io/pypi/l/wsstat.svg)](https://pypi.python.org/pypi/wsstat/)
[![PyPi](https://img.shields.io/pypi/pyversions/wsstat.svg)](https://pypi.python.org/pypi/wsstat/)


# Demo
![demo](https://cloud.githubusercontent.com/assets/1072598/19066857/48e13252-89d0-11e6-9ff3-ef2c69ae815e.gif)


# Installation
Note: wsstat currently only works on Python >= 3.3.

If you're on python >= 3.3 exclusively, it's as simple as:
```
pip install wsstat
```
Otherwise if you have python 2 & 3 installed it's
```
pip3 install wsstat
```

# Usage
```
$ wsstat -h
usage: wsstat [-h] [-n TOTAL_CONNECTIONS] [-c MAX_CONNECTING_SOCKETS]
                 [-H HEADER]
                 websocket_url

positional arguments:
  websocket_url         The websocket URL to hit

optional arguments:
  -h, --help            show this help message and exit
  -n TOTAL_CONNECTIONS, --num-clients TOTAL_CONNECTIONS
                        Number of clients to connect - default 250
  -c MAX_CONNECTING_SOCKETS, --max-connects MAX_CONNECTING_SOCKETS
                        Number of connections to simultaniously open - default
                        15
  -H HEADER, --header HEADER
                        Pass a custom header with each websocket connection
```
