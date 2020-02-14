import asyncio
from unittest import mock

from websockets import InvalidHandshake, InvalidURI, ConnectionClosed

from wsstat.clients import WebsocketTestingClient

class TestCoros(object):
    @asyncio.coroutine
    def bad_websocket_handshake(*args, **kwargs):
        raise InvalidHandshake("Bad status code: 200")

    @asyncio.coroutine
    def invalid_websocket_uri(*args, **kwargs):
        raise InvalidURI("Invalid URI specified!")

    @asyncio.coroutine
    def mock_sleep(*args, **kwargs):
        return

    @asyncio.coroutine
    def mocked_websocket(*args, **kwargs):
        class MockedWebsocket(mock.Mock):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.count = 0

            @asyncio.coroutine
            def recv(self, *args, **kwargs):
                self.count += 1
                if self.count > 3:
                    raise ConnectionClosed(1000, "Peace out homie!")
                return "Hello World!"

        return MockedWebsocket()


    def setup(self):
        self.identifier = "00000000"

        self.client = self._wrap_client(
            WebsocketTestingClient(
                websocket_url='wss://testserver/',
                total_connections=1,
                max_connecting_sockets=1,
                setup_tasks=False
            )
        )

    @mock.patch('wsstat.clients.websockets.connect', bad_websocket_handshake)
    @mock.patch('wsstat.clients.asyncio.sleep', mock_sleep)
    def test_bad_handshake(self):
        event_loop = asyncio.new_event_loop()
        try:
            assert len(asyncio.Task.all_tasks(event_loop)) == 0

            # Test bad handshakes
            event_loop.run_until_complete(self.client.create_websocket_connection())

            # Make sure that the logger was called
            assert self.client.logger.log.call_count > 0
            # Ensure that there was a failed connection
            assert isinstance(self.client.sockets[self.identifier], BaseException)
        finally:
            event_loop.stop()

    @mock.patch('wsstat.clients.websockets.connect', invalid_websocket_uri)
    @mock.patch('wsstat.clients.asyncio.sleep', mock_sleep)
    def test_invalid_ws_url(self):
        event_loop = asyncio.new_event_loop()
        try:
            assert len(asyncio.Task.all_tasks(event_loop)) == 0

            event_loop.run_until_complete(self.client.create_websocket_connection())

            # Make sure that the logger was called
            assert self.client.logger.log.call_count > 0
            # Ensure that there was a failed connection
            assert self.client.sockets[self.identifier] == False
        finally:
            event_loop.stop()

    @mock.patch('wsstat.clients.websockets.connect', mocked_websocket)
    def test_valid_connection(self):
        event_loop = asyncio.new_event_loop()
        try:
            # Test invalid URI
            event_loop.run_until_complete(self.client.create_websocket_connection())

            # Ensure logging was successful
            all_messages = self.arg_list_to_string(self.client.logger.log.call_args_list)
            assert "Connecting" in all_messages
            assert "Connected" in all_messages
            assert "Peace out homie!" in all_messages
            assert self.identifier in all_messages

            connected_websocket = self.client.sockets[self.identifier]
            assert connected_websocket.message_count == 3
            assert connected_websocket.id == self.identifier
            assert connected_websocket.last_message_recv != 0
            assert connected_websocket.ws is not None

            assert self.client.before_connect.call_count == 1
            assert self.client.setup_websocket_connection.call_count == 1
            assert self.client.get_identifier.call_count == 1
            assert self.client.after_connect.call_count == 1
            assert self.client.before_recv.call_count == 4
            assert self.client.after_recv.call_count == 3
        finally:
            event_loop.stop()



    def _wrap_client(self, client):
        # Wrap all the "hookable" functions to ensure they're called once and only once
        client.before_connect = mock.Mock(wraps=client.before_connect)
        client.setup_websocket_connection = mock.Mock(wraps=client.setup_websocket_connection)
        client.after_connect = mock.Mock(wraps=client.after_connect)
        client.before_recv = mock.Mock(wraps=client.before_recv)
        client.after_recv = mock.Mock(wraps=client.after_recv)

        # Intercept calls to the logger
        client.logger.log = mock.Mock(wraps=client.logger.log)

        # Use our static identifier
        client.get_identifier = mock.Mock(wraps=client.get_identifier, return_value=self.identifier)
        return client

    def arg_list_to_string(self, arglist):
        return " | ".join([x[0][0] for x in arglist])