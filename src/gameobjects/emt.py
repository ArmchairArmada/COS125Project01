#!/usr/bin/env python

from gameobject import GameObject
import assets
import components
import statevars

class EMT(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(EMT, self).__init__(scene, name, x, y, **kwargs)
        self.sprite = components.StaticSprite(self, assets.getImage("graphics/emt.png"), -32, -14)
        self.collider = components.SpriteCollide(self, -24, 1, 48, 16)
        self.save_collider = components.SpriteCollide(self, -16, -15, 32, 16)
        self.sound = assets.getSound("sounds/save.wav")

        self.save_delay = 5000
        self.save_timer = self.save_delay

    def init(self):
        """Initiation code."""
        self.obj_mgr.normal_update.append(self)
        self.obj_mgr.solid.add(self.collider)
        self.obj_mgr.player_touchable.add(self.save_collider)

    def destroy(self):
        """Clean up code."""
        self.sprite.destroy()
        self.obj_mgr.normal_update.remove(self)
        self.obj_mgr.solid.remove(self.collider)
        self.obj_mgr.player_touchable.remove(self.save_collider)

    def update(self, td):
        self.save_timer -= td

    def spriteCollide(self, gameobject, collider):
        if self.save_timer < 0:
            self.sound.play()
            self.save_timer = self.save_delay
            statevars.variables["map"]["spawn"] = self.name
            statevars.save()

    def spawnPlayer(self):
        player = self.obj_mgr.create("Player", "player", self.x, self.y - 10)
        player.spawn()

    def debug_draw(self, surface, camera_x, camera_y):
        super(EMT, self).debug_draw(surface, camera_x, camera_y)
        self.collider.debug_draw(surface, camera_x, camera_y)
        self.save_collider.debug_draw(surface, camera_x, camera_y)
