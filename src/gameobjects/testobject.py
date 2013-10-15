#!/usr/bin/env python

from gameobject import GameObject
import components
import assets
import pygame

class TestObject(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(TestObject, self).__init__(scene, name, x, y, **kwargs)

        # TODO: All of this should be put into a component, obviously
        #self.sprite = components.StaticSprite(self, assets.getImage("testing/test.png"))
        self.sprite = components.AnimSprite(self, assets.getSpriteAnim("testing/test_anim.json"))
        self.mapcollide = components.MapCollider(self, scene.tilemap.foreground, 0, 0, self.sprite.rect[2], self.sprite.rect[3])
        self.timeout = 5000

    def init(self):
        self.scene.object_mgr.normal_update.append(self)

    def destroy(self):
        self.sprite.destroy()
        self.scene.object_mgr.normal_update.remove(self)

    def update(self, td):
        keys = pygame.key.get_pressed()

        self.sprite.updateAnim(td)

        x = self.x
        y = self.y

        if keys[pygame.K_w]:
            y -= td * 0.1
        if keys[pygame.K_s]:
            y += td * 0.1
        if keys[pygame.K_a]:
            x -= td * 0.1
        if keys[pygame.K_d]:
            x += td * 0.1

        self.mapcollide.move(x,y)

        self.timeout -= td
        #if self.timeout <= 0:
        #    self.kill()

    def debug_draw(self, surface, camera_x, camera_y):
        super(TestObject, self).debug_draw(surface, camera_x, camera_y)
        self.sprite.debug_draw(surface, camera_x, camera_x)
        self.mapcollide.debug_draw(surface, camera_x, camera_y)
