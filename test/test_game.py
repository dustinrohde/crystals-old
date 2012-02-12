import pyglet
from pyglet.window import key

from crystals import game
from crystals import gui
from crystals import world
from crystals.world import entity
from test.util import *
from test.test_world import WorldTestCase


def TestGameMode():
    window = pyglet.window.Window()
    gamemode = game.GameMode(window)


def TestMainMenu():
    window = pyglet.window.Window()
    new_game = lambda: None
    mm = game.MainMenu(window, new_game)


class TestWorldMode(WorldTestCase):

    def setup(self):
        WorldTestCase.setup(self)

        self.window = pyglet.window.Window()
        self.room1 = self.roomgen.next()
        self.room2 = self.roomgen.next()
        self.rooms = {self.room1.name: self.room1, self.room2.name: self.room2}

        self.portals = {
            self.room1.name: {
                self.room2.name: (1, 2)},
            self.room2.name: {
                self.room1.name: (1, 1)}}

        self.world_ = world.World(self.rooms, self.portals,
                                  self.room2.name)
        self.player = entity.Entity(
            'player', False, 'cow.png', facing=(0, -1))
        self.world_.add_entity(self.player, 1, 1, 1)

        class MockPlot(object):
            app = None

        self.wmode = game.WorldMode(self.window, self.world_, self.player,
                                        MockPlot())

    def TestInit(self):
        pass

    def TestActivate(self):
        self.wmode.activate()

    def TestStepPlayer_NoPortalAtDest_MovePlayerGivenDistance(self):
        self.wmode.step_player(0, 1)
        assert self.room2[2][1][1] == self.player

    def TestStepPlayer_PortalAtDest_MovePlayerToPortalDest(self):
        self.wmode.step_player(0, 1)
        self.wmode.step_player(0, -1)
        assert self.room2[1][1][1] != self.player
        assert self.room1[2][1][1] == self.player

    def TestPortalPlayer_ValidCoordsGiven_AddPlayerToPortalDest(self):
        x, y, z = self.room2.get_coords(self.wmode.player)
        self.wmode.portal_player(x, y)
        x, y = self.world_.portals_dest2xy[self.room1.name][self.room2.name]
        assert self.room1[y][x][z] == self.wmode.player

    def TestPortalPlayer_ValidCoordsGiven_DelPlayerFromPrevPos(self):
        x, y, z = self.room2.get_coords(self.wmode.player)
        self.wmode.portal_player(x, y)
        assert self.room2[y][x][z] != self.wmode.player

    def TestPortalPlayer_ValidCoordsGiven_SetFocusToNewRoom(self):
        x, y, z = self.room2.get_coords(self.wmode.player)
        self.wmode.portal_player(x, y)
        assert self.world_.focus == self.room1

    def TestInteract_AlertAction_ActionExecutes(self):
        self.wmode.interact()

    def TestOnKeyPress_MovementKeyPressedAndWalkable_MovePlayer(self):
        x, y, z = self.world_.focus.get_coords(self.wmode.player)
        self.wmode.on_key_press(key.MOTION_UP, 0)
        assert self.room2[y + 1][x][z] == self.player

    def TestOnKeyPress_MovementKeyPressedButUnWalkable_DoNothing(self):
        for mvkey in (key.MOTION_LEFT, key.MOTION_DOWN, key.MOTION_RIGHT):
            x, y, z = self.world_.focus.get_coords(self.wmode.player)
            self.wmode.on_key_press(mvkey, 0)
            assert self.room2[y][x][z] == self.player


class TestGame(object):

    def TestInit(self):
        game_ = game.Game()

    def TestNewGame_LoadWorldMode(self):
        game_ = game.Game()
        def on_draw():
            pass
        game_.window.push_handlers(on_draw)
        game_.new_game()
        assert isinstance(game_.wmode, game.WorldMode)
