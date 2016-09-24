import time

import collections
import urwid
from urwid import DEFAULT
from urwid import LIGHT_GREEN
import urwid.curses_display

from websockets.protocol import OPEN, CLOSING, CLOSED

def get_ws_status(websocket, connected, error):
    if websocket.ws.state == OPEN:
        out = time.time() - websocket.last_message_recv
        if out < 0.3:
            return 'connected_highlight', connected
        else:
            return 'connected', connected
    elif websocket.ws.state in (CLOSING, CLOSED):
        return 'error', error

class BlinkBoard(object):
    def __init__(self):
        self.top_string = urwid.Text("")
        self.bottom_string = urwid.Text("")

        self.widget = urwid.LineBox(
            urwid.Pile([
                urwid.Filler(self.top_string, 'top'),
                ('weight', 10, urwid.Filler(self.bottom_string, 'bottom')),
            ]),
            title='Websockets'
        )

    def generate_blinkers(self, connected_sockets):
        if connected_sockets:

            compact_dashboard = []
            for websocket_id, websocket in connected_sockets.items():
                if websocket is None:
                    compact_dashboard.append(('starting', "*"))
                else:
                    compact_dashboard.append(get_ws_status(websocket, "C", "E"))

            message_counts = []
            active_sockets = [x for x in connected_sockets.values() if x]
            active_sockets.sort(key=lambda x: x.ws.state)

            for socket in active_sockets:
                status_string = get_ws_status(socket, socket.id[:8], socket.id[:8])

                message_counts.append(status_string)
                message_counts.append(":{} ".format(str(socket.message_count).ljust(4)))


            self.set_top_string(compact_dashboard)
            self.set_bottom_string(message_counts)
            # self.set_top_string("Nothing yet...")
            # self.set_bottom_string("Nothing yet...")

    def set_top_string(self, text):
        if text:
            self.top_string.set_text(text)

    def set_bottom_string(self, text):
        if text:
            self.bottom_string.set_text(text)

class Logger(object):
    log_messages = []

    timelogger = collections.deque(maxlen=30)

    graph_title = " Messages / Second | 3 Second window "

    def __init__(self):
        self.walker = urwid.SimpleFocusListWalker(contents=self.log_messages)
        self.list_box = urwid.ListBox(self.walker)



        satt = {(1, 0): 'bg 1 smooth', (2, 0): 'bg 2 smooth'}
        self.graph = urwid.BarGraph(['bg background', 'bg 1', 'bg 2'], satt=satt)

        self.graph_box = urwid.LineBox(self.graph, title=self.graph_title)

        self.widget = urwid.Columns([
            urwid.LineBox(
                self.list_box,
                title="Logger"
            ),
            self.graph_box
        ])

    def log(self, string):
        self.walker.append(urwid.Text(string))
        self.list_box.set_focus(len(self.list_box.body) - 1)

    def update_graph_data(self, data):
        self.timelogger.append(int(float(data[0])))
        graph_data = [[x] for x in self.timelogger]
        top = max([x[0] for x in graph_data])
        if top > 0:
            self.graph.set_data(graph_data, top)
            self.graph_box.title_widget.set_text(self.graph_title + "| Y-Max:{} ".format(top))
        else:
            self.graph_box.title_widget.set_text(self.graph_title)

palette = [
    ('banner', LIGHT_GREEN, DEFAULT),
    ('starting', 'white', ''),
    ('connected', 'black', 'dark green'),
    ('connected_highlight', 'black', 'white'),
    ('error', 'black', 'dark red'),
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('line',         'black',      'light gray', 'standout'),
        ('bg background','light gray', 'black'),
        ('bg 1',         'black',      'dark blue', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 2 smooth',  'dark cyan',  'black'),
        ('button normal','light gray', 'dark blue', 'standout'),
        ('button select','white',      'dark green'),
        ('line',         'black',      'light gray', 'standout'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
        ('pg smooth',     'dark magenta','black')
]

class DummyScreen(urwid.raw_display.Screen):
    def draw_screen(self, xxx_todo_changeme, r ):
        # profiler.run(super(DummyScreen, self).draw_screen, 'ch', args=(xxx_todo_changeme, r))
       pass

# screen = DummyScreen()
screen = urwid.raw_display.Screen()

def build_urwid_loop(client):
    frame = urwid.Frame(
        urwid.Pile(client.widgets),
        footer=urwid.Text("", align='center'),
    )

    client.frame = frame

    return urwid.MainLoop(
        frame,
        screen=screen,
        palette=palette,
        event_loop=urwid.AsyncioEventLoop(loop=client.loop),
        unhandled_input=client.unhandled_input
    )
