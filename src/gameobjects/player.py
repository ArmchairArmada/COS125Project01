#!/usr/bin/env python

"""
The player
"""

from gameobject import GameObject

class Player(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(Player, self).__init__(scene, name, x, y, **kwargs)

