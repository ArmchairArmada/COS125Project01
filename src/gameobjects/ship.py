#!/usr/bin/env python

"""
The ship is how the player arrives on the planet.  It is the starting spawn point.
"""

from gameobject import GameObject
import components
import assets
import statevars

class Ship(GameObject):
    def __init__(self, scene, name, x, y, direction=0, **kwargs):
        super(Ship, self).__init__(scene, name, x, y, **kwargs)
        self.ship_sprite = components.StaticSprite(self, assets.getImage("graphics/ship.png"))
        self.jet_sprite = components.AnimSprite(self, assets.getSpriteAnim("graphics/jet.json"), "jet", 16, 122)
        self.sound = assets.getSound("sounds/jet.wav")
        self.speed = 0.1
        self.dest_y = y - self.ship_sprite.rect[3] + 17
        self.x = x - self.ship_sprite.rect[2] / 2 + 8
        map = statevars.variables.get("map")
        if map is not None and map.get("ship_landed") == True:
            self.y = self.dest_y
            self.jet_sprite.setVisibility(False)
        else:
            self.y = -256
            self.sound.play(-1)

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
                self.sound.stop()
                self.y = self.dest_y
                self.jet_sprite.setVisibility(False)
                self.spawnPlayer()
                statevars.variables["map"]["ship_landed"] = True

    def spawnPlayer(self):
        statevars.variables["map"]["spawn"] = self.name
        player = self.obj_mgr.create("Player", "player", self.x + 32, self.y + 100)
        player.physics.applyForce(0.15, -0.1)

    def debug_draw(self, surface, camera_x, camera_y):
        super(Ship, self).debug_draw(surface, camera_x, camera_y)
        self.ship_sprite.debug_draw(surface, camera_x, camera_y)
        if self.jet_sprite.visible:
            self.jet_sprite.debug_draw(surface, camera_x, camera_y)
