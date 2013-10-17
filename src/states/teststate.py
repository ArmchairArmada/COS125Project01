#!/usr/bin/env python

import pygame
from states.gamestate import State
import scene

class TestState(State):
    """State for testing state manager"""
    def __init__(self):
        super(TestState, self).__init__()
        self.scene = scene.Scene(self, "testing/test.tmx")
        self.scene.object_mgr.create("test", None, 100, 100)

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        pass

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.scene.camera.y -= 0.25 * td

        if keys[pygame.K_DOWN]:
            self.scene.camera.y += 0.25 * td

        if keys[pygame.K_LEFT]:
            self.scene.camera.x -= 0.25 * td

        if keys[pygame.K_RIGHT]:
            self.scene.camera.x += 0.25 * td

        self.scene.update(td)

    def draw(self, surface):
        self.scene.draw(surface)
        self.scene.debug_draw(surface)

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE:
                self.scene.object_mgr.clear()

        return True