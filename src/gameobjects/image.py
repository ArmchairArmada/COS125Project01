#!/usr/bin/env python

"""Simple image game object -- it's just a still picture that sits there."""

from gameobject import GameObject
from components import StaticImage

import assets

class Image(GameObject):
    def __init__(self, scene, name, x, y, imageFile, **kwargs):
        super(Image, self).__init__(scene, name, x, y)
        self.static_image = StaticImage(assets.getImage(imageFile))
        self.width = self.static_image.image.get_width()
        self.height = self.static_image.image.get_height()

    def draw(self, surface, x, y):
        self.static_image.draw(surface, self.x + x, self.y + y)
