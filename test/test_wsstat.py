# coding=utf-8

import hashlib
from pytest import raises
from wsstat.clients import WebsocketTestingClient, ConnectedWebsocketConnection, \
    WebsocketTestingClientWithRandomApiTokenHeader
from wsstat.gui import WSStatConsoleApplication
from wsstat.main import parse_args


class TestsMisc(object):
    def test_coroutines(self):
        self.client = WebsocketTestingClient('wss://testserver/', total_connections=3, max_connecting_sockets=3)
        # Make sure we have len(total_connections) + redraw coroutine tasks
        assert len(self.client.coros) == (1 + self.client.total_connections)
        with raises(SystemExit, message="Expecting SystemExit"):
            self.client.exit()

class TestConnectedWebsocketConnection:
    def setup(self):
        self.token = hashlib.sha256(b'derp').hexdigest()
        self.socket = ConnectedWebsocketConnection(None, self.token)

    def test_message_increment(self):
        assert self.socket.message_count == 0

        self.socket.increment_message_counter()

        assert self.socket.message_count == 1

        self.socket.increment_message_counter()

        assert self.socket.message_count == 2

    def test_socket_as_string(self):
        assert str(self.socket) == "<Websocket {}>".format(self.socket.id)

    def test_message_handling(self):
        self.socket.process_message("Testing")
        assert self.socket.message_count == 1

    def test_building_objects(self):
        args = parse_args()

        client = WebsocketTestingClientWithRandomApiTokenHeader(**vars(args))

        application = WSStatConsoleApplication(client)


class TestParsing(object):
    import sys
    ws_url = 'wss://testserver/'

    sys.argv = [sys.argv[0], ws_url]

    args = parse_args()

    assert args.max_connecting_sockets == 15
    assert args.total_connections == 250
    assert args.websocket_url == ws_url