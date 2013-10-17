#!/usr/bin/env python

"""
Sprite components
"""

import pygame
import animation


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, gameobject, image, offset_x=0, offset_y=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = image.get_rect()
        self.gameobject = gameobject
        self.offset_x = offset_x
        self.offset_y = offset_y
        gameobject.obj_mgr.visible.add(self)

    def update(self, camera_x, camera_y):
        self.rect[0] = int(self.gameobject.x + self.offset_x + camera_x)
        self.rect[1] = int(self.gameobject.y + self.offset_y + camera_y)

    def destroy(self):
        self.gameobject.obj_mgr.visible.remove(self)

    def debug_draw(self, surface, camera_x, camera_y):
        pygame.draw.rect(surface, (255,0,0), self.rect, 1)


class AnimSprite(StaticSprite):
    def __init__(self, gameobject, anim, sequence, offset_x=0, offset_y=0):
        StaticSprite.__init__(self, gameobject, anim.getSequence(sequence).frames[0][0], offset_x, offset_y)
        self.animation = anim
        self.cursor = animation.SimpleCursor()
        self.cursor.play(anim.getSequence(sequence))

    def play(self, sequence_name, reset = True):
        self.cursor.play(self.animation.getSequence(sequence_name), reset)

    def updateAnim(self, td):
        self.cursor.update(td)
        self.image = self.cursor.frame
