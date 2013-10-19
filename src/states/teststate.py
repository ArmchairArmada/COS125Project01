#!/usr/bin/env python

import pygame
from states.gamestate import State
import scene
import inputs
import statemgr
import energybar

class TestState(State):
    """State for testing state manager"""
    def __init__(self):
        super(TestState, self).__init__()
        self.scene = scene.Scene(self, "testing/test.tmx")
        #obj = self.scene.object_mgr.create("Player", "player", 100, 100)
        #self.scene.camera.follow(obj)
        self.energy_bar = energybar.EnergyBar(None, 4, 4)

    def setPlayer(self, player):
        self.energy_bar.setHealth(player.health)

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        pass

    def loseFocus(self, next, next_name, *args, **kwargs):
        """What should be done when the state loses focus.  Next is the new state that is being switched to."""
        pass

    def update(self, td):
        if inputs.getPausePress():
            statemgr.switch("pause")
        self.scene.update(td)
        self.energy_bar.update()

    def draw(self, surface):
        self.scene.draw(surface)
        self.energy_bar.draw(surface)

    def debug_draw(self, surface):
        self.scene.debug_draw(surface)

    def event(self, event):
        """Should return true if game is still playing and false if the window should close"""
        return True