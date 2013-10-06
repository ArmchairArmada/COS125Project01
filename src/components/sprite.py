#!/usr/bin/env python

"""
Sprite Component
"""

import animation

class Sprite:
    def __init__(self, x = 0.0, y = 0.0, anim = None):
        self.x = x
        self.y = y

        self.cursor = animation.SimpleCursor()
        self.cursor.play(anim)

    def play(self, animation):
        self.cursor.play(animation)

    def update(self, td):
        self.cursor.update(td)

    def draw(self, surface, x, y):
        surface.blit(self.cursor.frame, (int(self.x + x), int(self.y + y)))
