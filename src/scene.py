#!/usr/bin/env python

"""
The scene contains a camera, game objects, and effects.
"""

import pygame
import gameobjects
import metrics

class Scene:
    def __init__(self):
        self.obj_mgr = gameobjects.ObjectManager()
        self.camera = gameobjects.Camera(self.obj_mgr, "camera", 0, 0, metrics.SCREEN_WIDTH, metrics.SCREEN_HEIGHT)

        self.collision_sprites = pygame.sprite.Group()

    def update(self, td):
        self.obj_mgr.update(td)

    def draw(self, surface):
        self.obj_mgr.draw(surface, -self.camera.x, -self.camera.y)
