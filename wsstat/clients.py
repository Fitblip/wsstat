# coding=utf-8
import asyncio
import hashlib
import itertools
import os
import time
import urllib
import urllib.parse
from ssl import CertificateError

import urwid
import websockets
import websockets.handshake

from collections import OrderedDict, deque
from websockets.protocol import OPEN
from wsstat.gui import BlinkBoardWidget, LoggerWidget

import logging

class ConnectedWebsocketConnection(object):
    def __init__(self, ws, identifier):
        self.ws = ws
        self.id = identifier
        self._message_count = itertools.count()
        self.last_message_recv = 0
        self.started = time.time()

    @property
    def message_count(self):
        return int(repr(self._message_count)[6:-1])

    def increment_message_counter(self):
        next(self._message_count)

    def __repr__(self):
        return "<Websocket {}>".format(self.id)

    def process_message(self, message):
        self.increment_message_counter()
        self.last_message_recv = time.time()


class WebsocketTestingClient(object):
    """
    Setting up the websocket calls the following callbacks that can be overridden to extend functinality.
    For an example see WebsocketTestingClientWithApiTokenHeader

    def before_connect(self):
    def setup_websocket_connection(self, statedict):
    def get_identifier(self, statedict):
    def after_connect(self, statedict):

    def before_recv(self, statedict):
    def after_recv(self, statedict, message):
    """

    def __init__(self, websocket_url, total_connections=250, max_connecting_sockets=5, setup_tasks=True):
        # Configuration stuff
        self.frame = None
        self.websocket_url = urllib.parse.urlparse(websocket_url)
        self.total_connections = total_connections
        self._exiting = False

        # Asyncio stuff
        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(self.handle_exceptions)
        self.connection_semaphore = asyncio.Semaphore(max_connecting_sockets)

        # Counts and buffers
        self.global_message_counter = itertools.count()
        self.sockets = OrderedDict()
        self.ring_buffer = deque(maxlen=10)

        if setup_tasks:
            self.setup_tasks()

        self.blinkboard = BlinkBoardWidget()
        self.logger = LoggerWidget()
        self.default_view = urwid.Pile([
            self.blinkboard.default_widget,
            (10, self.logger.default_widget)
        ])

        self.logger_view = urwid.Pile([
            self.logger.logger_widget,
        ])

        self.graph_view = urwid.Pile([
            self.logger.graph_widget,
        ])

        self.small_blink_and_graph_view = urwid.Pile([
            self.logger.graph_widget,
            (10, urwid.LineBox(self.blinkboard.small_blinks)),
        ])

    @property
    def messages_per_second(self):
        return self._get_current_messages_per_second()

    def log(self, identifier, message):
        self.logger.log("[{}] {}".format(identifier, message))

    @asyncio.coroutine
    def create_websocket_connection(self):
        statedict = self.before_connect()

        connection_args = self.setup_websocket_connection(statedict)

        # Make len(connection_semaphore) connection attempts at a time
        with (yield from self.connection_semaphore):
            identifier = self.get_identifier(statedict)

            self.log(identifier, 'Connecting to {}'.format(connection_args['uri']))

            start_time = time.time()

            # Signify that this socket is connecting
            self.sockets[identifier] = None

            try:
                # Await the connection to complete successfully
                websocket = yield from websockets.connect(**connection_args)
                websocket.connection_time = time.time() - start_time
            except BaseException as e:
                if isinstance(e, CertificateError):
                    self.logger.log("[{}] SSL connection problem! {}".format(identifier, e))
                else:
                    self.logger.log("[{}] {}".format(identifier, e))

                self.sockets[identifier] = False
                return False

            # Create our handler object
            connected_websocket = ConnectedWebsocketConnection(websocket, identifier)

            statedict['connected_websocket'] = connected_websocket

            # Update the connected_sockets table
            self.sockets[identifier] = connected_websocket

            # Log that we connected successfully
            self.logger.log("[{}] Connected in {:.4f} ms".format(connected_websocket.id, websocket.connection_time * 1000.00))

            self.after_connect(statedict)

        try:
            # Just loop and recv messages
            while True:
                if self._exiting:
                    yield from websocket.close()
                    return True

                self.before_recv(statedict)

                # Wait for a new message
                message = yield from websocket.recv()

                self.after_recv(statedict, message)

                # Increment our counters
                next(self.global_message_counter)

                connected_websocket.process_message(message)

        except Exception as e:
            # Log the exception
            self.logger.log("[{}] {}".format(connected_websocket.id, e))
            return False

    @asyncio.coroutine
    def update_urwid(self):
        interval = .1
        status_line = "{hostname} | Connections: [{current}/{total}] | Total Messages: {message_count} | Messages/Second: {msgs_per_second}/s"

        while True:
            if self._exiting:
                return True
                #raise urwid.ExitMainLoop

            # Only update things a max of 10 times/second
            yield from asyncio.sleep(interval)

            # Get the current global message count
            global_message_count = int(repr(self.global_message_counter)[6:-1])
            self.ring_buffer.append(global_message_count)

            currently_connected_sockets = len([x for x in self.sockets.values() if x and x.ws.state == OPEN])

            self.logger.update_graph_data([self.messages_per_second,])

            # Get and update our blinkboard widget
            self.blinkboard.generate_blinkers(self.sockets)
            # Make the status message
            status_message = status_line.format(
                hostname=self.websocket_url.netloc,
                current=currently_connected_sockets,
                total=self.total_connections,
                message_count=global_message_count,
                msgs_per_second=self.messages_per_second
            )
            self.frame.footer.set_text(status_message)

    def setup_tasks(self):
        tasks = []
        for _ in range(self.total_connections):
            coro = self.create_websocket_connection()
            tasks.append(asyncio.ensure_future(coro))

        update_urwid_coro = self.update_urwid()
        tasks.append(asyncio.ensure_future(update_urwid_coro))

        self.future = asyncio.gather(*tasks)

        # Gather all the tasks needed
        self.coros = tasks

    def exit(self):
        self._exiting = True
        import sys
        sys.exit(0)

    def handle_keypresses(self, keypress):
        if keypress == "q" or keypress == 'ctrl c':
            self.exit()

        keymap = {
            "l": self.logger_view,
            "g": self.graph_view,
            "tab": self.small_blink_and_graph_view,
            "esc": self.default_view
        }

        try:
            requested_view = keymap[keypress]
        except KeyError:
            return True

        if self.frame.body == requested_view:
            self.frame.body = self.default_view
        else:
            self.frame.body = requested_view

        return True

    def _get_current_messages_per_second(self):
        # Calculate deltas over the past window
        deltas = [y - x for x, y in zip(list(self.ring_buffer), list(self.ring_buffer)[1:])]

        # If the deque isn't empty
        if deltas:
            msgs_per_second = '{0:.2f}'.format(float(sum(deltas) / len(self.ring_buffer)) * 10)
        else:
            msgs_per_second = '{0:.2f}'.format(float(0.0))

        return msgs_per_second

    def before_recv(self, statedict):
        pass

    def after_recv(self, statedict, message):
        pass

    def before_connect(self):
        statedict = {}
        return statedict

    def after_connect(self, statedict):
        pass

    def setup_websocket_connection(self, statedict):
        return {
            "uri": self.websocket_url.geturl(),
        }

    def get_identifier(self, statedict):
        return hashlib.sha256(os.urandom(4)).hexdigest()[:8]

    def handle_exceptions(self, loop, context):
        logging.error("Exception! : {}".format(str(context.get('exception'))))

class WebsocketTestingClientWithRandomApiTokenHeader(WebsocketTestingClient):
    """
    Introduces a new parameter: `header_name` - used to specify the key to 'extra_headers' passed to `websocket.connect`
    """
    def __init__(self, *args, **kwargs):
        self.header_name = kwargs.pop("header_name", 'x-endpoint-token')
        super().__init__(*args, **kwargs)

    def before_connect(self):
        statedict = super().before_connect()

        # Generate a random API token
        statedict['api_token'] = hashlib.sha256(os.urandom(4)).hexdigest()

        return statedict

    def setup_websocket_connection(self, statedict):
        args = super().setup_websocket_connection(statedict)
        args['extra_headers'] = {
            self.header_name: statedict['api_token']
        }
        return args

    def get_identifier(self, statedict):
        return statedict['api_token'][:8]