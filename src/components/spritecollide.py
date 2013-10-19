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
        self.rect = pygame.Rect(gameobject.x + offset_x, gameobject.y + offset_y, width, height)

    def addToGroup(self, group):
        group.add(self)

    def removeFromGroup(self, group):
        group.remove(self)

    def update(self):
        self.rect[0] = self.gameobject.x + self.offset_x
        self.rect[1] = self.gameobject.y + self.offset_y

    def touch(self, gameobject, collider, *args, **kwargs):
        self.gameobject.call("spriteCollide", gameobject, collider, *args, **kwargs)

    def collide(self, group, *args, **kwargs):
        # TODO: Figure out if this is what I actually want.
        for spr in pygame.sprite.spritecollide(self, group, False):
            spr.touch(self.gameobject, self,  *args, **kwargs)

    def debug_draw(self, surface, camera_x, camera_y):
        pygame.draw.rect(surface, (255,0,255), (self.gameobject.x + self.offset_x + camera_x, self.gameobject.y + self.offset_y + camera_y, self.width, self.height), 1)
