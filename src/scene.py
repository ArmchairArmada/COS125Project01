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

class SceneManager:
    """Manages updating, drawing, and transitioning between scenes

    Initializes using the following state variables:
        save_scene, save_x, save_y

    These are the last places the player has saved his game's progress.

    TODO:
        Allow for cut scenes
    """
    def __init__(self):
        self.player = gameobjects.Player(None, "player", statevars.variables["save_x"], statevars.variables["save_y"])
        self.camera = gameobjects.Camera(None, "camera", 0, 0, metrics.SCREEN_WIDTH, metrics.SCREEN_HEIGHT)

        self.scene = Scene(self, self.player, self.camera)
        self.scene.load(statevars.variables["save_scene"])
        self.previous_scene = None

        self.camera.jumpTo(self.player)
        self.camera.follow(self.player)

    def transition(self, filename):
        self.previous_scene = self.scene
        self.scene = Scene(self.player, self.camera)
        self.previous_scene.focus = False

    def update(self, td):
        if self.previous_scene:
            self.previous_scene.update(td)
            if not self.previous_scene.isVisible():
                self.previous_scene = None
        self.scene.update(td)

    def draw(self, surface):
        if self.previous_scene:
            self.previous_scene.draw(surface)
        self.scene.draw(surface)


class Scene:
    """This is where the game's action happens."""
    def __init__(self, sceneMgr, player, camera):
        self.sceneMgr = sceneMgr
        self.obj_mgr = gameobjects.ObjectManager()
        self.camera = camera
        self.camera.scene = self
        self.player = player
        self.player.scene = self

        # Boundaries of scene
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        self.left_scene = "None"
        self.right_scene = "None"
        self.top_scene = "None"
        self.bottom_scene = "None"

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

        # Scenes to transition to if moving off current scene
        self.left_scene = data["left_scene"]
        self.right_scene = data["right_scene"]
        self.top_scene = data["top_scene"]
        self.bottom_scene = data["bottom_scene"]

        self._loadScene(data["scene"])

    def _loadScene(self, data):
        for entry in data:
            if entry["type"] == "create":
                obj = gameobjects.create(entry["class"], self, entry["name"], entry["x"], entry["y"], **entry["kwargs"])

            if entry["type"] == "if":
                if entry["comparison"] == "==":
                    if statevars.variables[entry["variable"]] == entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "<":
                    if statevars.variables[entry["variable"]] < entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "<=":
                    if statevars.variables[entry["variable"]] <= entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == ">":
                    if statevars.variables[entry["variable"]] > entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == ">=":
                    if statevars.variables[entry["variable"]] >= entry["value"]:
                        self._loadScene(entry["then"])
                elif entry["comparison"] == "!=":
                    if statevars.variables[entry["variable"]] != entry["value"]:
                        self._loadScene(entry["then"])
                else:
                    pass

    def update(self, td):
        self.obj_mgr.update(td)
        if self.focus:
            self.player.update(td)
            self.camera.update(td)

    def draw(self, surface):
        self.obj_mgr.draw(surface, -self.camera.x, -self.camera.y)
        if self.focus:
            self.player.draw(surface, -self.camera.x, -self.camera.y)
            self.camera.draw(surface, -self.camera.x, -self.camera.y)

    def isVisible(self):
        """Check if scene dimensions overlap with the camera"""
        return self.rect.colliderect(self.camera.rect)
