# coding=utf-8
import collections
import time
import urwid
import urwid.curses_display

from websockets.protocol import OPEN, CLOSING, CLOSED

palette = [
    ('starting', 'white', ''),
    ('starting_text', 'black', 'yellow'),
    ('connected', 'black', 'dark green'),
    ('connected_highlight', 'black', 'white'),
    ('error', 'black', 'dark red'),

    ('graph bg background','light gray', 'black'),
    ('graph bg 1',         'black',      'dark blue', 'standout'),
    ('graph bg 1 smooth',  'dark blue',  'black'),
    ('graph bg 2',         'black',      'dark cyan', 'standout'),
    ('graph bg 2 smooth',  'dark cyan',  'black'),
]

class WSStatConsoleApplication(object):
    # Used for debugging (doesn't actuall render screen output while calculating everyhting)
    class DummyScreen(urwid.raw_display.Screen):
        def draw_screen(self, xxx_todo_changeme, r):
            pass

    class FixedAsyncLoop(urwid.AsyncioEventLoop):
        def run(self):
            """
            Start the event loop.  Exit the loop when any callback raises
            an exception.  If ExitMainLoop is raised, exit cleanly.
            """
            try:
                self._loop.run_forever()
            except (KeyboardInterrupt, SystemExit):
                pass

    def __init__(self, client):
        self.client = client

        self.screen = urwid.raw_display.Screen()
        # self.screen = self.DummyScreen()

        self.frame = urwid.Frame(
            client.default_view,
            footer=urwid.Text("", align='center'),
        )

        self.client.frame = self.frame

        self.urwid_loop = urwid.MainLoop(
            self.frame,
            screen=self.screen,
            palette=palette,
            event_loop=self.FixedAsyncLoop(loop=client.loop),
            unhandled_input=client.handle_keypresses,
            pop_ups=True
        )

    def run(self):
        self.urwid_loop.run()
        import sys
        sys.exit(0)

class BlinkBoardWidget(object):
    def __init__(self):
        self.top_string = urwid.Text('')
        self.bottom_string  = urwid.Text('')

        self.small_blinks = urwid.Filler(self.top_string, 'top')
        self.large_blinks = ('weight', 10, urwid.Filler(self.bottom_string, 'top'))

        self.default_widget = urwid.LineBox(
            urwid.Pile([
                self.large_blinks
            ]),
            title='Websockets'
        )

    def generate_blinkers(self, connected_sockets):
        if connected_sockets:
            small_blinkers = []
            large_blinkers = []
            for websocket_id, websocket in connected_sockets.items():
                if websocket is None:
                    small_blinkers.append(('starting', "*"))
                    large_blinkers.append(('starting_text', "{}".format(websocket_id)))
                    large_blinkers.append(":_    ")

                else:
                    small_blinkers.append(self.get_ws_status(websocket, "C", "E"))

                    large_blinkers.append(self.get_ws_status(websocket, websocket.id[:8], websocket.id[:8]))
                    large_blinkers.append(":{} ".format(str(websocket.message_count).ljust(4)))

            self.update_small_blinkers(small_blinkers)
            self.update_large_blinkers(large_blinkers)

    def update_small_blinkers(self, blinkers):
        if blinkers:
           self.top_string.set_text(blinkers)

    def update_large_blinkers(self, blinkers):
        if blinkers:
            self.bottom_string.set_text(blinkers)

    def get_ws_status(self, websocket, connected, error):
        if websocket is False:
            return 'error', error
        elif websocket.ws.state == OPEN:
            out = time.time() - websocket.last_message_recv
            if out < 0.3:
                return 'connected_highlight', connected
            else:
                return 'connected', connected
        elif websocket.ws.state in (CLOSING, CLOSED):
            return 'error', error

class LoggerWidget(object):
    log_messages = []

    timelogger = collections.deque(maxlen=30)

    graph_title = " Messages / Second | 3 Second window "

    def __init__(self):
        self.walker = urwid.SimpleFocusListWalker(contents=self.log_messages)
        self.list_box = urwid.ListBox(self.walker)

        self.graph = urwid.BarGraph(
            attlist=['graph bg background', 'graph bg 1', 'graph bg 2'],
            satt={
                (1, 0): 'graph bg 1 smooth',
                (2, 0): 'graph bg 2 smooth'
            }
        )

        self.graph_widget = urwid.LineBox(self.graph, title=self.graph_title)

        self.default_widget = urwid.Columns([
            urwid.LineBox(
                self.list_box,
                title="Logger"
            ),
            self.graph_widget
        ])

        self.logger_widget = urwid.LineBox(
            self.list_box,
            title="Logger"
        )


    def log(self, string):
        self.walker.append(urwid.Text(string))
        self.list_box.set_focus(len(self.list_box.body) - 1)

    def update_graph_data(self, data):
        self.timelogger.append(int(float(data[0])))
        graph_data = [[x] for x in self.timelogger]
        top = max([x[0] for x in graph_data])
        if top > 0:
            self.graph.set_data(graph_data, top)
            self.graph_widget.title_widget.set_text(self.graph_title + "| Y-Max:{} ".format(top))
        else:
            self.graph_widget.title_widget.set_text(self.graph_title)
