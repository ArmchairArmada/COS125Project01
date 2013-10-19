#!/usr/bin/env python

"""
The Pause state pauses the game and displays a darkened view of the old state
"""

from states import State
import statemgr
import inputs
import assets
import statevars

class TitleState(State):
    """Base class for all game states to derive from"""
    def __init__(self):
        super(TitleState, self).__init__()
        self.image = assets.getImage("graphics/title.png")

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        pass

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        if inputs.getPausePress():
            statevars.load("saves/save_1.json")
            statemgr.switch("play")

    def draw(self, surface):
        surface.blit(self.image, (0,0))

    def debug_draw(self, surface):
        pass

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        return True
