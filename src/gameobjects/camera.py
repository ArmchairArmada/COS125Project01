#!/usr/bin/env python

from gameobject import GameObject
import metrics

DIRECT = 0
FOLLOW = 1

class Camera(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(Camera, self).__init__(scene, name, x, y)
        self.width = metrics.SCREEN_WIDTH
        self.height = metrics.SCREEN_HEIGHT
        self.offset_x = -self.width / 2
        self.offset_y = -self.height / 2
        self.target = None
        self.state = DIRECT

    def follow(self, target, target_offset_x=0, target_offset_y=0):
        self.target = target
        self.target_offset_x = target_offset_x
        self.target_offset_y = target_offset_y
        self.state = FOLLOW

    def update(self, td):
        if self.state == DIRECT:
            pass
        elif self.state == FOLLOW:
            self.x = self.target.x + self.offset_x + self.target_offset_x
            self.y = self.target.y + self.offset_y + self.target_offset_y

        self.x = min(max(self.x, 0), self.scene.tilemap.pixel_width - self.width)
        self.y = min(max(self.y, 0), self.scene.tilemap.pixel_height - self.height)

    def goto(self, x, y):
        self.state = DIRECT
        self.x = x + self.offset_x
        self.y = y + self.offset_y

    def move(self, x, y):
        self.state = DIRECT
        self.x += x
        self.y += y
