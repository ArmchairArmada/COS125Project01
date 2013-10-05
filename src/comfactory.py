#!/usr/bin/env python

"""
Game Object Component Factory
"""

import components

_component_classes = {
    "Sprite": components.Sprite
}

def create(name, *args, **kwargs):
    com = _component_classes.get(name)
    if com:
        return com(*args, **kwargs)
