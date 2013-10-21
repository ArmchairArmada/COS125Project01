#!/usr/bin/env python

"""
A purple tentacle
"""

from enemy import Enemy

ANIM_WALK = 0
ANIM_HURT = 1

class Tentacle(Enemy):
    def __init__(self, scene, name, x, y, **kwargs):
        super(Tentacle, self).__init__(scene, name, x, y, "anims/tenticle.json", "walk_r", 24, 32, spr_offset_x=-4, health=50, **kwargs)
        if self.facing == 1:
            self.sprite.play("walk_r")
        else:
            self.sprite.play("walk_l")
        self.walk_speed = 0.0002
        self.anim_state = ANIM_WALK

    def enemyUpdate(self, td):
        self.updateState(td)

    def updateState(self, td):
        turn = False

        if self.mapcollider.on_ground:
            ground_in_front = self.checkForEdge()

            if self.mapcollider.hit_left or self.mapcollider.hit_right or ground_in_front:
                self.facing = -self.facing
                turn = True

            self.physics.applyForce(self.walk_speed * td * self.facing, 0)

        self.updateAnim(td, turn)

    def doDamage(self, amount):
        super(Tentacle, self).doDamage(amount)
        self.anim_state = ANIM_HURT
        if self.facing == 1:
            self.sprite.play("hurt_r")
        else:
            self.sprite.play("hurt_l")

    def updateAnim(self, td, turn):
        if self.anim_state == ANIM_WALK:
            if turn:
                if self.facing == 1:
                    self.sprite.play("walk_r")
                else:
                    self.sprite.play("walk_l")
        elif self.anim_state == ANIM_HURT:
            if not self.sprite.cursor.playing:
                self.anim_state = ANIM_WALK
                if self.facing == 1:
                    self.sprite.play("walk_r")
                else:
                    self.sprite.play("walk_l")
