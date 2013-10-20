#!/usr/bin/env python

"""
Since there will only be one state manager and it needs to be accessed by many
things, this has been made global.
"""

import states

_states = {}
_state = None
_state_name = ""

_previous = None
_previous_name = ""


def init():
    global _states

    _states = {
        "test":states.TestState(),
        "pause":states.PauseState(),
        "title":states.TitleState(),
        "play":states.PlayState(),
        "dialog":states.DialogState()
    }


def switch(state_name, *args, **kwargs):
    """Switch to a different game state"""
    global _states, _state, _state_name, _previous, _previous_name

    new_state = _states[state_name]

    if _state:
        _state.has_focus = False
        _state.loseFocus(new_state, state_name, *args, **kwargs)

    _previous = _state
    _previous_name = _state_name
    _state = new_state
    _state_name = state_name
    _state.has_focus = True
    _state.gainFocus(_previous, _previous_name, *args, **kwargs)


def update(td):
    _state.update(td)


def draw(surface):
    _state.draw(surface)


def debug_draw(surface):
    _state.debug_draw(surface)


def event(event):
    return _state.event(event)
