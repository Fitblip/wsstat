import hashlib

from wsstat.main import WebsocketTestingClient, ConnectedWebsocketConnection

class Tests(object):
    def setup(self):
        self.client = WebsocketTestingClient('wss://testserver/', total_connections=3, max_connecting_sockets=3)

    def test_coroutines(self):
        print(self.client)
        assert len(self.client.tasks._children) == (1 + self.client.total_connections)


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

