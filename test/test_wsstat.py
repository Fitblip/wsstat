
from wsstat.main import client
import urwid

def test_nop():
    assert isinstance(client.blinkboard.bottom_string, urwid.Text)