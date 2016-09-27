# coding=utf-8

import hashlib
from unittest import mock

import pytest

from wsstat.clients import ConnectedWebsocketConnection, WebsocketTestingClient
from wsstat.gui import WSStatConsoleApplication
from wsstat.main import parse_args, wsstat_console


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

def test_parsing_arguments():
    import sys
    ws_url = 'wss://testserver/'

    sys.argv = [sys.argv[0], ws_url]

    args = parse_args()

    assert args.max_connecting_sockets == 15
    assert args.total_connections == 250
    assert args.websocket_url == ws_url

@mock.patch('wsstat.main.WSStatConsoleApplication')
@mock.patch('wsstat.main.WebsocketTestingClientWithRandomApiTokenHeader')
def test_client_setup(console_class, client_class):
    wsstat_console()

@mock.patch('wsstat.gui.urwid.MainLoop')
def test_client_run(mainloop):
    client = WebsocketTestingClient(
        websocket_url='wss://testserver/',
        total_connections=1,
        max_connecting_sockets=1,
        setup_tasks=False
    )
    console = WSStatConsoleApplication(client)

    assert WSStatConsoleApplication.DummyScreen().draw_screen(None, None) == None

    with pytest.raises(SystemExit):
        console.run()

    assert client.messages_per_second == '0.00'

def test_fixed_async_loop():
    def raise_KeyboardInterrupt():
        raise KeyboardInterrupt
    def raise_SystemExit():
        raise SystemExit
    def raise_generic_Exception():
        raise Exception

    loop = WSStatConsoleApplication.FixedAsyncLoop()

    loop._loop.run_forever = raise_KeyboardInterrupt
    loop.run()

    loop._loop.run_forever = raise_SystemExit
    loop.run()

    loop._loop.run_forever = raise_generic_Exception
    with pytest.raises(Exception):
        loop.run()
