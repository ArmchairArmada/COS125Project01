#!/usr/bin/env python

from gameobject import GameObject
import assets
import components
import statevars
import statemgr

class Coin(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(Coin, self).__init__(scene, name, x, y)
        self.sprite = components.AnimSprite(self, assets.getSpriteAnim("anims/coin.json"), "spin")
        self.collider = components.SpriteCollide(self, 0, 0, 16, 16)
        self.sound = assets.getSound("sounds/coin.wav")

    def init(self):
        """Initiation code."""
        self.obj_mgr.normal_update.append(self)
        self.collider.addToGroup(self.obj_mgr.player_touchable)
        if self.name in statevars.variables["map"].get("coins", []):
            self.kill()

    def destroy(self):
        """Clean up code."""
        self.obj_mgr.normal_update.remove(self)
        self.sprite.destroy()
        self.collider.removeFromGroup(self.obj_mgr.player_touchable)

    def update(self, td):
        self.sprite.updateAnim(td)

    def spriteCollide(self, gameobject, collider):
        self.sound.play()
        self.kill()
        if statevars.variables["map"].get("coins") == None:
            statevars.variables["map"]["coins"] = [self.name]
        else:
            statevars.variables["map"]["coins"].append(self.name)
        statemgr.get("play").getCoin()

    def debug_draw(self, surface, camera_x, camera_y):
        super(Coin, self).debug_draw(surface, camera_x, camera_y)
        self.sprite.debug_draw(surface, camera_x, camera_y)
        self.collider.debug_draw(surface, camera_x, camera_y)
