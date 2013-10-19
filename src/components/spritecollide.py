#!/usr/bin/env python

"""
Sprite collision component

game object needs a spriteCollide method if it is going to collide
"""

import pygame

class SpriteCollide(pygame.sprite.Sprite):
    def __init__(self, gameobject, offset_x, offset_y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.gameobject = gameobject
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)

    def addToGroup(self, group):
        group.add(self)

    def removeFromGroup(self, group):
        group.remove(self)

    def update(self):
        self.rect[0] = self.gameobject.x + self.offset_x
        self.rect[1] = self.gameobject.y + self.offset_y

    def touch(self, *args, **kwargs):
        self.gameobject.call("spriteCollide", *args, **kwargs)

    def collide(self, group, *args, **kwargs):
        # TODO: Figure out if this is what I actually want.
        for spr in pygame.sprite.spritecollide(self, group, False):
            spr.touch(self, *args, **kwargs)
