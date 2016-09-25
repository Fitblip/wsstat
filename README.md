# WSStat: Making websocket monitoring beautiful

[![Build Status](https://travis-ci.org/Fitblip/wsstat.svg?branch=master)](https://travis-ci.org/Fitblip/wsstat)
[![Coverage Status](https://coveralls.io/repos/github/Fitblip/wsstat/badge.svg?branch=master)](https://coveralls.io/github/Fitblip/wsstat?branch=master)
[![PyPi](https://img.shields.io/pypi/dm/wsstat.svg)](https://pypi.python.org/pypi/wsstat/)
[![PyPi](https://img.shields.io/pypi/v/wsstat.svg)](https://pypi.python.org/pypi/wsstat/)




# Demo
![demo](https://cloud.githubusercontent.com/assets/1072598/18814490/bb2fb2b0-82c9-11e6-8a35-6b80c0f40dc3.gif)


# Installation
Note: wsstat currently only works on Python >= 3.4.

If you're on python3.5 exclusively, it's as simple as:
```
pip install wsstat
```
Otherwise if you have python 2 & 3 installed it's
```
pip3 install wsstat
```

# Usage
```
$ python3.5 main.py -h
usage: main.py [-h] [-n NUM_CLIENTS] [-c MAX_CONNECTS] websocket_url

positional arguments:
  websocket_url         The websocket URL to hit

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_CLIENTS, --num-clients NUM_CLIENTS
                        Number of clients to connect - default 250
  -c MAX_CONNECTS, --max-connects MAX_CONNECTS
                        Number of connections to simultaniously open - default 15
```
