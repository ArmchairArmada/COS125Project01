#!/usr/bin/env python

"""Camera class"""

import pygame
from gameobject import GameObject

NORMAL = 0
FOLLOW = 1

class Camera(GameObject):
    def __init__(self, scene, name, x, y, width, height, **kwargs):
        super(Camera, self).__init__(scene, name, x, y)
        self.target = None
        # width and height should be screen dimensions in pixels
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)
        self.state = NORMAL

    def follow(self, target):
        self.target = target
        self.state = FOLLOW

    def jumpTo(self, target):
        pass

    def update(self, td):
        if self.state == FOLLOW:
            self.x = self.target.x - self.target.width / 2 + self.width / 2
            self.y = self.target.y - self.target.height / 2 + self.height / 2

        self.rect[0] = int(self.x)
        self.rect[1] = int(self.y)
