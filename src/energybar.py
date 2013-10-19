#!/usr/bin/env python

"""
Displays energy levels onto the screen
"""

import assets

class EnergyBar:
    def __init__(self, health, x, y):
        self.health = health
        self.x = x
        self.y = y
        self.background = assets.getImage("graphics/energy_background.png")
        self.foreground = assets.getImage("graphics/energy_bar.png")
        self.bar = self.foreground
        self.energy = self.health.health

    def update(self):
        if self.energy != self.health.health:
            self.energy = self.health.health
            percent = float(self.health.health) / self.health.max_health
            width = int(self.foreground.get_width() * percent)
            height = self.foreground.get_height()
            self.bar = self.foreground.subsurface(0, 0, width, height)

    def draw(self, surface):
        surface.blit(self.background, (self.x, self.y))
        surface.blit(self.bar, (self.x + 34, self.y + 2))
