#!/usr/bin/env python

"""
Sprite components
"""

import pygame
import assets


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, gameobject, imagefile, offset_x=0, offset_y=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets.getImage(imagefile)
        self.rect = self.image.get_rect()
        self.gameobject = gameobject
        self.offset_x = offset_x
        self.offset_y = offset_y
        gameobject.obj_mgr.visible.add(self)

    def update(self, camera_x, camera_y):
        self.rect[0] = int(self.gameobject.x + self.offset_x + camera_x)
        self.rect[1] = int(self.gameobject.y + self.offset_y + camera_y)

    def destroy(self):
        self.gameobject.obj_mgr.visible.remove(self)


# TODO: Animated sprite
# TODO: Make animation controller used by AnimSprite
