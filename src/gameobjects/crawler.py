#!/usr/bin/env python

from enemy import Enemy

class Crawler(Enemy):
    def __init__(self, scene, name, x, y, **kwargs):
        super(Crawler, self).__init__(scene, name, x, y, "anims/crawler.json", "walk_r", 24, 16, health=10, **kwargs)
        self.walk_speed = 0.005

    def enemyUpdate(self, td):
        self.updateState(td)
        self.updateAnim(td)

    def updateState(self, td):
        turn = False
        ground_in_front = self.mapcollider.getHeight(self.x + self.mapcollider.width / 2 + self.facing * 8, self.y, 24)

        if self.mapcollider.hit_left or self.mapcollider.hit_right or ground_in_front == self.y + 24:
            self.facing = -self.facing
            turn = True

        if turn:
            if self.facing == 1:
                self.sprite.play("walk_r")
            else:
                self.sprite.play("walk_l")

        if self.mapcollider.on_ground:
            self.physics.applyForce(self.walk_speed * td * self.facing, 0)

    def updateAnim(self, td):
        pass
