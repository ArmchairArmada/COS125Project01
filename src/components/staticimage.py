#!/usr/bin/env python

class StaticImage:
    def __init__(self, image):
        self.image = image

    def update(self, td):
        pass

    def draw(self, surface, x, y):
        surface.blit(self.image, (int(x), int(y)))
