"""top-level game logic"""
import pyglet
from pyglet.window import key

from crystals.loaders import WorldLoader
from crystals.loaders import DATA_PATH, RES_PATH
from crystals.gui import Menu

# Use the data/ and res/ directories in the test suite when debugging
if __debug__:
    from test.helpers import DATA_PATH, RES_PATH

class GameMode(object):

    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()


class MainMenu(GameMode, Menu):

    def __init__(self, window, new_game):
        GameMode.__init__(self, window)
        Menu.__init__(
            self, 0, 0, window.width, window.height, self.batch,
            ['new game', 'quit'],
            [new_game, pyglet.app.exit],
            show_box=True, bold=True)


class Game(object):

    def __init__(self):
        self.win_width = 600
        self.win_height = 400
        self.window = pyglet.window.Window(self.win_width, self.win_height)
        self.window.clear()

        self.main_menu = MainMenu(self.window, self.new_game)
        self.world = None

    def run(self):
        self.window.push_handlers(self.main_menu)
        pyglet.app.run()

    def new_game(self):
        self.window.pop_handlers()
        self.window.clear()
        loader = WorldLoader(DATA_PATH, RES_PATH)
        self.world = loader.load_room('TestRoom1')
