#!/usr/bin/env python

"""
Sprite Component
"""

import animation
import assets

class Sprite:
    def __init__(self, game_obj, offset_x = 0.0, offset_y = 0.0, anim = None):
        self.game_obj = game_obj
        game_obj.updatable_components.append(self)
        game_obj.drawable_components.append(self)
        self.x = game_obj.x
        self.y = game_obj.y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cursor = animation.SimpleCursor()
        if anim:
            self.cursor.play(assets.getSpriteAnim(anim))

    def play(self, animation):
        self.cursor.play(animation)

    def update(self, td):
        pass

    def lateUpdate(self, td):
        self.x = self.game_obj.x + self.offset_x
        self.y = self.game_obj.y + self.offset_y

        self.cursor.update(td)

    def draw(self, surface, x, y):
        surface.blit(self.cursor.frame, (int(self.x - x), int(self.y - y)))
