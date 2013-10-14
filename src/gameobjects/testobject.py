#!/usr/bin/env python

from gameobject import GameObject
import pygame
import components
import assets

class TestObject(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(TestObject, self).__init__(scene, name, x, y, **kwargs)

        # TODO: All of this should be put into a component, obviously
        #self.sprite = components.StaticSprite(self, assets.getImage("testing/test.png"))
        self.sprite = components.AnimSprite(self, assets.getSpriteAnim("testing/test_anim.json"))
        self.timeout = 5000

    def init(self):
        self.scene.object_mgr.normal_update.append(self)

    def destroy(self):
        self.sprite.destroy()
        self.scene.object_mgr.normal_update.remove(self)

    def update(self, td):
        self.sprite.updateAnim(td)
        self.x += td * 0.02
        self.timeout -= td
        if self.timeout <= 0:
            self.kill()

    def debug_draw(self, surface, camera_x, camera_y):
        super(TestObject, self).debug_draw(surface, camera_x, camera_y)
        self.sprite.debug_draw(surface, camera_x, camera_x)
