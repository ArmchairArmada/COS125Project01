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
        self.sprite = components.AnimSprite(self, assets.getSpriteAnim("graphics/player.json"), "run_r", -16, -16)
        self.mapcollide = components.MapCollider(self, scene.tilemap.foreground, -5, -8, 11, 24)
        #self.mapcollide = components.MapCollider(self, scene.tilemap.foreground, 0, 0, 32, 32)
        self.physics = components.Physics(self, self.mapcollide, 0.03)
        self.timeout = 5000
        self.dir = 1

    def init(self):
        self.scene.object_mgr.normal_update.append(self)

    def destroy(self):
        self.sprite.destroy()
        self.scene.object_mgr.normal_update.remove(self)

    def update(self, td):
        keys = pygame.key.get_pressed()

        self.sprite.updateAnim(td)

        jumping = False
        if self.mapcollide.on_ground and keys[pygame.K_w]:
            #self.physics.applyForce(0, -0.1 * td)
            self.physics.setForceY(-0.45)
            #self.physics.setForceY(-0.2)
            jumping = True
        #if keys[pygame.K_s]:
        #    self.physics.applyForce(0, 0.1 * td)
        if self.mapcollide.on_ground and keys[pygame.K_a]:
            self.physics.applyForce(-0.004 * td, 0)
            if self.dir == 1:
                self.dir = 0
                self.sprite.play("run_l")
        if self.mapcollide.on_ground and keys[pygame.K_d]:
            self.physics.applyForce(0.004 * td, 0)
            if self.dir == 0:
                self.dir = 1
                self.sprite.play("run_r")

        #self.mapcollide.move(x,y)
        was_on_ground = self.mapcollide.on_ground

        if not jumping and was_on_ground:
            self.physics.setForceY(8.0 / (td+0.001))

        self.physics.update(td)

        if not jumping and not self.mapcollide.on_ground and was_on_ground:
            self.physics.setForceY(0.0)

        self.timeout -= td
        #if self.timeout <= 0:
        #    self.kill()

    def debug_draw(self, surface, camera_x, camera_y):
        super(TestObject, self).debug_draw(surface, camera_x, camera_y)
        self.sprite.debug_draw(surface, camera_x, camera_x)
        self.mapcollide.debug_draw(surface, camera_x, camera_y)
        self.physics.debug_draw(surface, camera_x, camera_y)
