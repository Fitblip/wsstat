#!/usr/bin/env python
# coding=utf-8
import argparse

from wsstat.clients import WebsocketTestingClient
from wsstat.demo import DemoClient
from wsstat.gui import WSStatConsoleApplication

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "websocket_url",
        nargs='?',
        help="The websocket URL to hit",
        default=""
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
        help="Number of connections attempted simultaneously - default 15",
        dest="max_connecting_sockets",
        action="store",
        default="15",
        type=int
    )
    parser.add_argument(
        '-H', "--header",
        help="Pass a custom header with each websocket connection",
        dest="header",
        action="store",
        default=None,
        type=str
    )
    parser.add_argument(
        "--demo",
        help="Start a demo websocket server and point wsstat at it",
        dest="demo",
        action="store_true"
    )

    parser.add_argument(
       '-i', "--insecure",
        help="Don't validate SSL certificates on websocket servers",
        dest="insecure",
        action="store_true"
    )

    args = parser.parse_args()

    if not args.websocket_url and not args.demo:
        parser.error("You must specify a websocket url if not in demo mode!")

    return args

def wsstat_console():
    args = parse_args()

    if args.demo:
        client = DemoClient(**vars(args))
    else:
        client = WebsocketTestingClient(**vars(args))

    application = WSStatConsoleApplication(client)

    application.run()
