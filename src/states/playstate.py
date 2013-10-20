#!/usr/bin/env python

from states.gamestate import State
import scene
import inputs
import statemgr
import energybar
import statevars
import pygame

class PlayState(State):
    def __init__(self):
        super(PlayState, self).__init__()
        self.init = True
        self.help_text="""                                  ~yellow~*** HELP ***~white~
In ~yellow~Cat Astro Fee ~white~you play as an astronaut who happens to
also be a cat.  Why is he a cat?  For the pun, of course!
On each planet, he has to collect enough ~yellow~coins ~white~to pay to
get past the ~yellow~space toll booths~white~.

Controls can be configured in ~yellow~data/config.json~white~, but the
default settings are ~yellow~keyboard ~white~with the '~yellow~ARROW KEYS~white~' to move,
'~yellow~Z~white~' to jump, '~yellow~X~white~' to shoot, and '~yellow~ENTER~white~' to pause the game.
~yellow~EMTs~white~ (Emergency Medical Teleporters) are used to save your
progress and act as checkpoints you can respawn at after
losing all your health.
Watch out for enemies, spikes, lava, and other hazards.
If you take damage, a refreshing ~yellow~Fish Soda~white~ refills a
little bit of health.
After collecting all the ~yellow~coins~white~ in the level, return to the
~yellow~space ship~white~ to blast off and head to the next planet!
"""

    def setPlayer(self, player):
        self.energy_bar.setHealth(player.health)

    def respawn(self):
        statevars.load()
        self.start()

    def start(self):
        self.energy_bar = energybar.EnergyBar(None, 4, 4)
        map = statevars.variables.get("map")
        if map is None:
            map_file = "maps/start.tmx"
            map = {}
            statevars.variables["map"] = map
            map["filename"] = map_file
            map["spawn"] = None
            statevars.save()
        else:
            map_file = map.get("filename")
            if map_file is None:
                map_file = "maps/start.tmx"
        self.scene = scene.Scene(self, map_file)
        spawn = map.get("spawn")
        if spawn is not None:
            obj = self.scene.object_mgr.get(spawn)
            obj.call("spawnPlayer")

    def gainFocus(self, previous, previous_name, *args, **kwargs):
        """What should be done when the state gets focus.  Previous is the state that had focus before this one."""
        if self.init:
            self.init = False
            self.start()

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                statemgr.switch("dialog", text=self.help_text)
        return True
