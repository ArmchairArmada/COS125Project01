#!/usr/bin/env python

"""
Game States are the modes the game might be plyaing in  and could include things like title screen, game play,
pause screen, credits, etc.
"""

# TODO: unit tests

class GameStateMgr:
    def __init__(self):
        from statetest import TestState

        self.states = {
            "test":TestState(self)
        }

        self.state = None
        self.state_name = ""

        self.previous = None
        self.previous_name = ""

    def switch(self, state_name, *args, **kwargs):
        """Switch to a different game state"""
        new_state = self.states[state_name]

        if self.state:
            self.state.has_focus = False
            self.state.loseFocus(new_state, state_name, *args, **kwargs)

        self.previous = self.state
        self.previous_name = self.state_name
        self.state = new_state
        self.state_name = state_name
        self.state.has_focus = True
        self.state.gainFocus(self.previous, self.previous_name, *args, **kwargs)

    def update(self, td):
        self.state.update(td)

    def draw(self, surface):
        self.state.draw(surface)

    def event(self, event):
        return self.state.event(event)


class State(object):
    """Base class for all game states to derive from"""
    def __init__(self, state_mgr):
        super(State, self).__init__()
        self.state_mgr = state_mgr
        self.has_focus = False

    def switch(self, state_name, *args, **kwargs):
        self.state_mgr.switch(state_name, *args, **kwargs)

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        pass

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        pass

    def draw(self, surface):
        pass

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        return True
