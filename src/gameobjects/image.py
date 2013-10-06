#!/usr/bin/env python

"""Simple image game object -- it's just a still picture that sits there."""

from gameobject import GameObject
from components import StaticImage

import assets

class Image(GameObject):
    def __init__(self, objectMgr, name, x, y, imageFile):
        super(Image, self).__init__(objectMgr, name, x, y)
        self.static_image = StaticImage(assets.getImage(imageFile))

    def draw(self, surface, x, y):
        self.static_image.draw(surface, self.x + x, self.y + y)
