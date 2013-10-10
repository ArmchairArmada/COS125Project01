#!/usr/bin/env python

"""
The ObjectManager manages creating, updating, and drawing objects.
"""

import pygame
from gameobjects.testobject import TestObject

class ObjectManager:
    def __init__(self, scene):
        self.scene = scene
        self.objects = {}

        # Controls the order objects are updated
        self.early_update = []    # Early objects might include platforms entities can ride on
        self.normal_update = []   # Most entities will go here
        self.late_update = []     # Objects that need to be updated after everything, like the camera

        # Sprite groups for collision and drawing
        self.visible = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player_touchable = pygame.sprite.Group()
        self.enemy_touchable = pygame.sprite.Group()

        self.auto_name_id = 0

        self.to_add = []
        self.to_remove = []

        # Object classes for factory
        self.classes = {
            "test":TestObject
        }

    def _auto_name(self):
        self.auto_name_id += 1
        return "_obj_" + str(self.auto_name_id)

    def get(self, name):
        return self.objects.get(name)

    def add(self, name, obj):
        self.to_add.append((name, obj))

    def _add(self):
        # TODO: Should probably check if it overrides an existing object
        for name, obj in self.to_add:
            if name is None:
                name = self._auto_name()
                obj.name = name
            self.objects[name] = obj
            obj.init()
        self.to_add = []

    def remove(self, name):
        self.to_remove.append(name)

    def _remove(self):
        for name in self.to_remove:
            self.objects[name].destroy()
            del self.objects[name]
        self.to_remove = []

    def create(self, class_name, name, x, y, **kwargs):
        if name is None:
            name = self._auto_name()
        obj = self.classes[class_name](self.scene, name, x, y, **kwargs)
        self.add(name, obj)
        return obj

    def createFromTMX(self, tmx):
        # TODO: Import game objects from TMX object layer
        pass

    def clear(self):
        self.to_remove = self.objects.keys()

    def update(self, td):
        self._remove()
        self._add()

        for obj in self.early_update:
            obj.update(td)

        for obj in self.normal_update:
            obj.update(td)

        for obj in self.late_update:
            obj.update(td)

    def draw(self, surface):
        # Updates sprites rects relative to camera
        self.visible.update(-self.scene.camera.x, -self.scene.camera.y)
        self.visible.draw(surface)

    def debug_draw(self, surface):
        for obj in self.objects.itervalues():
            obj.debug_draw(surface)
