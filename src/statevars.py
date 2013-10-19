#!/usr/bin/env python

"""
Keeps track of game accomplishments, past events, and current state values.
"""

# Todo: Exception handling
# Todo: Logging

import assets

_filename = None
variables = {}

def load(filename=None):
    global variables, _filename

    if filename is None:
        filename = _filename
    variables = assets.getData(filename, False)
    _filename = filename

def save(filename=None):
    if filename is None:
        filename = _filename

    assets.saveData(variables, filename)
