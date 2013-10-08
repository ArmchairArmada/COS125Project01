#!/usr/bin/env python

"""
The game object is the root of our game.  It initializes PyGame, creates the window, and runs
"""

import pygame
import metrics
import assets
import gamestate

class Game:
    def __init__(self):
        self.config = assets.getData("config.json")
        self.scale = self.config["scale"]
        self.width = metrics.SCREEN_WIDTH * self.scale
        self.height = metrics.SCREEN_HEIGHT * self.scale

        fullscreen = 0
        if self.config["fullscreen"]:
            fullscreen = pygame.FULLSCREEN

        pygame.init()
        pygame.display.set_caption("Planetary Pitstops")  # TODO: Come up with better name
        self.display = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF | fullscreen)
        self.surface = pygame.Surface((metrics.SCREEN_WIDTH, metrics.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        self.state_mgr = gamestate.GameStateMgr()
        self.state_mgr.switch("test")

        self.playing = True

    def run(self):
        while self.playing:
            for event in pygame.event.get():
                self.playing = self.state_mgr.event(event)

            td = self.clock.tick(metrics.FPS)

            self.state_mgr.update(td)
            self.state_mgr.draw(self.surface)

            pygame.transform.scale(self.surface, (self.width, self.height), self.display)

            pygame.display.flip()

        pygame.quit()
