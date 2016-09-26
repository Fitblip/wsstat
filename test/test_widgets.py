import hashlib
import os
from unittest import mock

import time
from websockets.protocol import CONNECTING, OPEN, CLOSING, CLOSED
from wsstat.gui import BlinkBoardWidget

class TestBlinkBoardWidget(object):
    def generate_identifier(self):
        return hashlib.sha256(os.urandom(4)).hexdigest()[:8]

    def setup(self):
        self.blinkboard = BlinkBoardWidget()
        self.connected_sockets = {}
        self.connected_sockets[self.generate_identifier()] = None

        for state in [OPEN, CLOSING, CLOSED]:
            socket = mock.Mock()
            socket.ws.state = state
            socket.last_message_recv = time.time()
            socket.id = self.generate_identifier()
            self.connected_sockets[socket.id] = socket

    def test_update(self):
        self.blinkboard.generate_blinkers(connected_sockets=self.connected_sockets)