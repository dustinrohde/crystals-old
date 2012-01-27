"""interaction between the player and other entities"""


class Action(object):
    """An action that can be committed by an entity in the world."""

    def __init__(self, nactions):
        self.nactions = nactions
    
    def execute(self, entity):
        """Execute the action, given the entity responsible for it."""
        if self.nactions < 1:
            return
        self.nactions -= 1


class Alert(Action):
    """Action which writes something to an output stream, presumably
    the game's infobox."""

    def __init__(self, nactions, text):
        Action.__init__(self, nactions)
        self.text = text
