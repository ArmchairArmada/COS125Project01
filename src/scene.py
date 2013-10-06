#!/usr/bin/env python

"""
The scene contains a camera, game objects, and effects.

TODO:
    Add scene manager to handle transitions
"""

import pygame
import gameobjects
import metrics
import assets
import statevars
import json
import logging

class SceneManager:
    """Manages updating, drawing, and transitioning between scenes

    Initializes using the following state variables:
        save_scene, save_x, save_y

    These are the last places the player has saved his game's progress.

    TODO:
        Allow for cut scenes
        Add transition types (slide, fade, cut, etc.)  Maybe using temporary surfaces for some transitions
    """
    def __init__(self):
        self.scene = Scene(self)
        self.scene.load(statevars.variables["save_scene"])
        self.previous_scene = None

        self.player = gameobjects.Player(self.scene, "player", statevars.variables["save_x"], statevars.variables["save_y"])
        self.camera = gameobjects.Camera(self.scene, "camera", 0, 0, metrics.SCREEN_WIDTH, metrics.SCREEN_HEIGHT)

        self.camera.jumpTo(self.player)
        self.camera.follow(self.player)

    def transition(self, filename):
        self.previous_scene = self.scene
        self.scene = Scene(self)
        self.previous_scene.focus = False

    def update(self, td):
        if self.previous_scene:
            self.previous_scene.update(td)
            if not self.previous_scene.isVisible(self.camera):
                self.previous_scene = None
        self.scene.update(td)
        self.player.update(td)
        self.camera.update(td)

    def draw(self, surface):
        if self.previous_scene:
            self.previous_scene.draw(surface, -self.camera.x, -self.camera.y)
        self.scene.draw(surface, -self.camera.x, -self.camera.y)
        self.player.draw(surface, -self.camera.x, -self.camera.y)


class Scene:
    """This is where the game's action happens."""
    def __init__(self, sceneMgr):
        self.sceneMgr = sceneMgr
        self.obj_mgr = gameobjects.ObjectManager()

        # Boundaries of scene
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        self.focus = True

        self.collision_sprites = pygame.sprite.Group()

    def load(self, filename):
        # Load scene and configure objects from file
        file = assets.load(filename)
        data = json.load(file)
        file.close()

        # TODO: Use these while loading scene
        # data["tilemap"]
        # data["script"]

        self.left = data["left"]
        self.right = data["right"]
        self.top = data["top"]
        self.bottom = data["bottom"]

        self.rect = pygame.Rect(self.left, self.top, self.right - self.left, self.bottom - self.top)

        self._loadScene(data["scene"])

    def _loadScene(self, data):
        for entry in data:
            if entry["type"] == "create":
                obj = gameobjects.create(entry["class"], self, entry["name"], entry["x"], entry["y"], **entry["kwargs"])

            elif entry["type"] == "if":
                var = statevars.variables.get(entry["variable"])
                if entry["comparison"] == "exists":
                    if var:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "not_exists":
                    if var is None:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "==":
                    if var == entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "<":
                    if var and var < entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "<=":
                    if var and var <= entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == ">":
                    if var and var > entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == ">=":
                    if var and var >= entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "!=":
                    if var != entry["value"]:
                        self._loadScene(entry["then"])
                else:
                    logging.error("Invalid comparison type: %s" % entry["comparison"])

            elif entry["type"] == "set":
                statevars.variables[entry["variable"]] = entry["value"]

            elif entry["type"] == "call":
                obj = self.obj_mgr.get(entry["object"])
                if obj:
                    obj.call(entry["func"], entry["kwargs"])
                else:
                    logging.warning("Object %s does not exist" % entry["object"])

            else:
                pass

    def update(self, td):
        self.obj_mgr.update(td)

    def draw(self, surface, x, y):
        self.obj_mgr.draw(surface, x, y)

    def isVisible(self, camera):
        """Check if scene dimensions overlap with the camera"""
        return self.rect.colliderect(camera.rect)


if __name__ == "__main__":
    import testing

    testing.init()

    statevars.variables["save_scene"] = "test_scene.json"
    statevars.variables["save_x"] = 0
    statevars.variables["save_y"] = 0

    sm = SceneManager()

    def u(td):
        sm.update(td)
        testing.display.fill((255,255,255))
        sm.draw(testing.display)

    testing.loop(u)
