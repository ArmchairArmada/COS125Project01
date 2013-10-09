#!/usr/bin/env python

import pygame
from gamestate import State
import assets

class TestState(State):
    """State for testing state manager"""
    def __init__(self):
        super(TestState, self).__init__()
        self.image = assets.getImage("testing/test.png")

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        pass

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        pass

    def draw(self, surface):
        surface.blit(self.image, (0,0))

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
        return True