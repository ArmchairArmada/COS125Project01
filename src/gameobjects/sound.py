#!/usr/bin/env python

"""
Sound source
"""

from gameobject import GameObject
import assets

class Sound(GameObject):
    def __init__(self, scene, name, x, y, filename="", play=0, **kwargs):
        super(Sound, self).__init__(scene, name, x, y, **kwargs)
        self.sound = assets.getSound(filename)
        self.play(play)
        self.active = True

    def play(self, play=1):
        if play != 0:
            if play>0:
                self.sound.play(play-1)
            elif play == -1:
                self.sound.play(-1)

    def update(self, td):
        for msg, args, kwargs in self.subscriber.get():
            if msg == "pulse":
                self.play()
