#!/usr/bin/env python

"""
The scene contains a camera, game objects, and effects.

NOTE:
    A camera object should have the following components:
        - Follow: Moves to match target object
        - Shake: Applies a shaking effect, like during an earthquake
        - MoveTo: Moves to a specific location
"""

import gameobject

class Scene:
    def __init__(self):
        self.obj_mgr = gameobject.ObjectManager()
        self.camera = self.obj_mgr.createGameObject("Camera", 0, 0, "camera.json")

    def update(self, td):
        self.obj_mgr.update(td)

    def draw(self, surface):
        self.obj_mgr.draw(surface, self.camera.x, self.camera.y)
