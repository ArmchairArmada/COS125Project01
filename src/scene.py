#!/usr/bin/env python

"""
The scene contains a camera, game objects, and effects.
"""

import gameobjects

class Scene:
    def __init__(self):
        self.obj_mgr = gameobjects.ObjectManager()

    def update(self, td):
        self.obj_mgr.update(td)

    def draw(self, surface):
        self.obj_mgr.draw(surface, 0, 0)
