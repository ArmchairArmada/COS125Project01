#!/usr/bin/env python

from gameobject import GameObject
import pygame
import components

class TestObject(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(TestObject, self).__init__(scene, name, x, y, **kwargs)

        # TODO: All of this should be put into a component, obviously
        self.sprite = components.StaticSprite(self, "testing/test.png")
        self.timeout = 2000

    def init(self):
        self.scene.object_mgr.normal_update.append(self)

    def destroy(self):
        self.sprite.destroy()
        self.scene.object_mgr.normal_update.remove(self)

    def update(self, td):
        self.x += td * 0.01
        self.timeout -= td
        if self.timeout <= 0:
            self.kill()

    def debug_draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.sprite.rect, 1)
