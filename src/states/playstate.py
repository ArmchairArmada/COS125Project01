#!/usr/bin/env python

from states.gamestate import State
import scene
import inputs
import statemgr
import energybar
import statevars

class PlayState(State):
    def __init__(self):
        super(PlayState, self).__init__()
        self.init = True

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
        return True
