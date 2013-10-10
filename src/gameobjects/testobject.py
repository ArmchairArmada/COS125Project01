#!/usr/bin/env python

from gameobject import GameObject
import assets
import pygame


# TODO: Make real sprite component
class TmpSpr(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets.getImage("testing/test.png")
        self.rect = self.image.get_rect()
        self.parent = parent

    def update(self, x, y):
        self.rect[0] = int(self.parent.x+x)
        self.rect[1] = int(self.parent.y+y)



class TestObject(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(TestObject, self).__init__(scene, name, x, y, **kwargs)

        # TODO: All of this should be put into a component, obviously
        self.sprite = TmpSpr(self)
        self.timeout = 2000

    def init(self):
        self.scene.object_mgr.visible.add(self.sprite)
        self.scene.object_mgr.normal_update.append(self)

    def destroy(self):
        self.scene.object_mgr.visible.remove(self.sprite)
        self.scene.object_mgr.normal_update.remove(self)

    def update(self, td):
        self.x += td * 0.01
        self.timeout -= td
        if self.timeout <= 0:
            self.kill()

    def debug_draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.sprite.rect, 1)
