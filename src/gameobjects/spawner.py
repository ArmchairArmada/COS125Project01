#!/usr/bin/env python

"""
Spawns objects at a given interval with a random position within a rectangular area
"""

from gameobject import GameObject
import random

class Spawner(GameObject):
    def __init__(self, scene, name, x, y, width=0, height=0, obj="", rate=500, params={}, **kwargs):
        super(Spawner, self).__init__(scene, name, x, y)
        self.width = width
        self.height = height
        self.obj_name = obj
        self.rate = int(rate)
        self.timer = self.rate
        self.params = params

    def init(self):
        self.obj_mgr.normal_update.append(self)

    def destroy(self):
        self.obj_mgr.normal_update.remove(self)

    def update(self, td):
        self.timer -= td
        if self.timer < 0:
            self.timer = self.rate
            x = self.x + random.randrange(self.width)
            y = self.y + random.randrange(self.height)
            self.obj_mgr.create(self.obj_name, None, x, y, **self.params)

    def debug_draw(self, surface, camera_x, camera_y):
        super(Spawner, self).debug_draw(surface, camera_x, camera_y)
        import pygame
        pygame.draw.rect(surface, (128,255,0), (self.x + camera_x, self.y + camera_y, self.width, self.height), 1)
