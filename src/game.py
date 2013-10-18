#!/usr/bin/env python

"""
The game object is the root of our game.  It initializes PyGame, creates the window, and runs
"""

# TODO: Catch config loading exception and load defaults on error (maybe generate default file)

import pygame
import metrics
import assets
import statemgr
import inputs

class Game:
    def __init__(self):
        self.config = assets.getData("config.json")
        self.scale = self.config["scale"]
        self.width = metrics.SCREEN_WIDTH * self.scale
        self.height = metrics.SCREEN_HEIGHT * self.scale

        fullscreen = 0
        if self.config["fullscreen"]:
            fullscreen = pygame.FULLSCREEN

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.display.set_caption("Cat Astro Fee")  # TODO: Come up with better name
        pygame.display.set_icon(pygame.image.load(assets.path("graphics/icon.png")))
        pygame.mouse.set_visible(False)
        self.display = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF | fullscreen)
        self.surface = pygame.Surface((metrics.SCREEN_WIDTH, metrics.SCREEN_HEIGHT), pygame.HWSURFACE)

        self.clock = pygame.time.Clock()

        inputs.init(self.config)

        statemgr.init()
        statemgr.switch("test")

        self.playing = True

        self.debug_mode = False

    def run(self):
        while self.playing:
            for event in pygame.event.get():
                self.playing = statemgr.event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F12:
                        self.debug_mode = not self.debug_mode

                    if event.key == pygame.K_ESCAPE:
                        self.playing = False

                if event.type == pygame.QUIT:
                    self.playing = False

            td = self.clock.tick(metrics.FPS)

            if td > 100:
                td = 100

            inputs.update()
            statemgr.update(td)
            statemgr.draw(self.surface)

            if self.debug_mode:
                statemgr.debug_draw(self.surface)

            pygame.transform.scale(self.surface, (self.width, self.height), self.display)

            pygame.display.flip()

        pygame.quit()
