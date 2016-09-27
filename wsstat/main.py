#!/usr/bin/env python
# coding=utf-8
import argparse

from wsstat.clients import WebsocketTestingClientWithRandomApiTokenHeader
from wsstat.gui import WSStatConsoleApplication

def parse_args():
    parser = argparse.ArgumentParser(epilog="Note: this is very much so in flux right now so don't expect anything to remain the same!")
    parser.add_argument(
        "websocket_url",
        help="The websocket URL to hit"
    )
    parser.add_argument(
        "-n", "--num-clients",
        help="Number of clients to connect - default 250",
        dest='total_connections',
        action="store",
        default="250",
        type=int
    )
    parser.add_argument(
        "-c", "--max-connects",
        help="Number of connections to simultaniously open - default 15",
        dest="max_connecting_sockets",
        action="store",
        default="15",
        type=int
    )
    args = parser.parse_args()
    return args

def wsstat_console():
    args = parse_args()

    client = WebsocketTestingClientWithRandomApiTokenHeader(**vars(args))

    application = WSStatConsoleApplication(client)

    application.run()
