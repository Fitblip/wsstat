<p align="center">
  <a href="https://pypi.python.org/pypi/wsstat/">
    <img alt="wsstat" src="https://cloud.githubusercontent.com/assets/1072598/19067433/0657350a-89d3-11e6-92ef-9e20fd8245ac.png" width="546">
  </a>
</p>

<p align="center">
  Websocket stress testing made beautiful
</p>

<p align="center">
    <a href="https://travis-ci.org/Fitblip/wsstat"><img src="https://travis-ci.org/Fitblip/wsstat.svg?branch=master" alt="Build Status" data-canonical-src="https://travis-ci.org/Fitblip/wsstat.svg?branch=master" style="max-width:100%;"></a>
    <a href="https://coveralls.io/github/Fitblip/wsstat?branch=master"><img src="https://coveralls.io/repos/github/Fitblip/wsstat/badge.svg?branch=master" alt="Coverage Status" data-canonical-src="https://coveralls.io/repos/github/Fitblip/wsstat/badge.svg?branch=master" style="max-width:100%;"></a>
    <a href="https://pypi.python.org/pypi/wsstat/"><img src="https://img.shields.io/pypi/v/wsstat.svg" alt="PyPi" data-canonical-src="https://img.shields.io/pypi/v/wsstat.svg" style="max-width:100%;"></a>
    <a href="https://pypi.python.org/pypi/wsstat/"><img src="https://img.shields.io/pypi/l/wsstat.svg" alt="PyPi" data-canonical-src="https://img.shields.io/pypi/l/wsstat.svg" style="max-width:100%;"></a>
    <a href="https://pypi.python.org/pypi/wsstat/"><img src="https://img.shields.io/pypi/pyversions/wsstat.svg" alt="PyPi" data-canonical-src="https://img.shields.io/pypi/pyversions/wsstat.svg" style="max-width:100%;"></a>
</p>


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
