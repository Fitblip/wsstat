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

#### Hello!

This repository holds WSStat, a websocket monitoring and visualization tool written in Python 3.3+, using the great AsyncIO, Websocket, and Urwid libraries 😎 .

It aims to make diagnosing problems and understanding your websocket infrastructure easy and beautiful.

There are still a few edges and whatnot since it's fairly new, and some functionality doesn't exist (yet), but that's where I'm hoping the community can help.

#### I'm actively looking for feedback

The core of WSStat was written to be modular with extensibility in mind. Want a web API to gather statistics while it runs? How about a websocket server that pushes statistics from multiple workers to one place? Threshold based alerting? Slack integration? File a ticket and we'll kick it around!

It should go without saying, but pull requests are *absolutely* welcome!

#### Now, a demo

![demo](https://cloud.githubusercontent.com/assets/1072598/22418901/d9f2d00e-e68f-11e6-9443-7fdd9a23ba01.gif)

When you pass the `--demo` flag to WSStat, it will spin up an asynchronous websocket server on port `65432` point the websocket monitors to that server, allowing you to see functionality with a real websocket server.

#### Installation
Install from pip - `pip install wsstat`

**Note:** if you have python 2 and 3 installed on the same system, you have to use `pip3 install wsstat`!

The installation should be 100% straight forward and work fine. If that's not the case, please file a ticket!

Please note: WSStat currently only works on Python >= 3.3, and won't install on python 2.7, which is a known limitation.

#### Usage

Using wsstat is pretty straight forward, and it only has a few knobs (for now). If you want to try wsstat out and don't have a websocket infrastructure handy, you can just pass in `--demo` to have wsstat set up a server for you!

Other than that, you can adjust the total number of connected clients with `-n`, the number of simultaneous sockets trying to connect at once with `-c`, or pass in an arbitrary header (for things like authentication) with `-H`.

```
$ wsstat -h
usage: wsstat [-h] [-n TOTAL_CONNECTIONS] [-c MAX_CONNECTING_SOCKETS]
              [-H HEADER] [--demo] [-i]
              [websocket_url]

positional arguments:
  websocket_url         The websocket URL to hit

optional arguments:
  -h, --help            show this help message and exit
  -n TOTAL_CONNECTIONS, --num-clients TOTAL_CONNECTIONS
                        Number of clients to connect - default 250
  -c MAX_CONNECTING_SOCKETS, --max-connects MAX_CONNECTING_SOCKETS
                        Number of connections attempted simultaneously -
                        default 15
  -H HEADER, --header HEADER
                        Pass a custom header with each websocket connection
  --demo                Start a demo websocket server and point wsstat at it
  -i, --insecure        Don't validate SSL certificates on websocket servers
```

#### Usage example

Connect a total of 30 clients by attempting to open five simultaneous sockets at `wss://echo.websocket.org`

```
$ wsstat wss://echo.websocket.org -n 30 -c 5
```
