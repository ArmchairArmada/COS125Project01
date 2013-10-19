#!/usr/bin/env python

from gameobject import GameObject
import components
import assets

class Ship(GameObject):
    def __init__(self, scene, name, x, y, direction=0, **kwargs):
        super(Ship, self).__init__(scene, name, x, y, **kwargs)
        self.ship_sprite = components.StaticSprite(self, assets.getImage("graphics/ship.png"))
        self.jet_sprite = components.AnimSprite(self, assets.getSpriteAnim("graphics/jet.json"), "jet", 16, 122)
        self.dest_y = y - self.ship_sprite.rect[3] + 17
        self.x = x - self.ship_sprite.rect[2] / 2 + 8
        self.y = -256
        self.speed = 0.1

    def init(self):
        """Initiation code."""
        self.obj_mgr.normal_update.append(self)

    def destroy(self):
        """Clean up code."""
        self.ship_sprite.destroy()
        self.jet_sprite.destroy()
        self.obj_mgr.normal_update.remove(self)

    def update(self, td):
        if self.y < self.dest_y:
            self.jet_sprite.updateAnim(td)
            self.y += self.speed * td
            if self.y > self.dest_y:
                self.y = self.dest_y
                self.jet_sprite.setVisibility(False)
                self.spawnPlayer()

    def spawnPlayer(self):
        player = self.obj_mgr.create("Player", "player", self.x + 32, self.y + 100)
        player.physics.applyForce(0.15, -0.1)

    def debug_draw(self, surface, camera_x, camera_y):
        super(Ship, self).debug_draw(surface, camera_x, camera_y)
