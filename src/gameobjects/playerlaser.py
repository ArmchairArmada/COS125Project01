#!/usr/bin/env python

from gameobject import GameObject
import components
import assets

class PlayerLaser(GameObject):
    def __init__(self, scene, name, x, y, direction=0, **kwargs):
        super(PlayerLaser, self).__init__(scene, name, x, y, **kwargs)
        if direction == 0:
            self.sprite = components.StaticSprite(self, assets.getImage("graphics/laser_l.png"), -4, -3)
            self.speed = -0.5
        else:
            self.sprite = components.StaticSprite(self, assets.getImage("graphics/laser_r.png"), -4, -3)
            self.speed = 0.5
        self.collider = components.SpriteCollide(self, -4, -3, 8, 5)
        self.mapcollider = components.MapCollider(self, scene.tilemap.foreground, -4, -3, 8, 5)
        self.damage_amount = 25
        self.sound = assets.getSound("sounds/laser.wav")
        self.sound.play()

    def init(self):
        """Initiation code."""
        self.obj_mgr.normal_update.append(self)
        self.obj_mgr.enemy_touchable.add(self.collider)

    def destroy(self):
        """Clean up code."""
        self.sprite.destroy()
        self.obj_mgr.normal_update.remove(self)
        self.obj_mgr.enemy_touchable.remove(self.collider)

    def update(self, td):
        h_collide, v_collide = self.mapcollider.move(self.x + self.speed * td, self.y)
        if h_collide or v_collide:
            self.kill()
        if self.x < -100 or self.x > self.scene.width + 100:
            self.kill()

    def spriteCollide(self, gameobject, collider):
        gameobject.call("doDamage", self.damage_amount)
        self.sound.play()
        self.kill()

    def debug_draw(self, surface, camera_x, camera_y):
        super(PlayerLaser, self).debug_draw(surface, camera_x, camera_y)
        self.collider.debug_draw(surface, camera_x, camera_y)
        self.mapcollider.debug_draw(surface, camera_x, camera_y)
