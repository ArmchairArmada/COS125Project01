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
        if name is None:
            name = self._auto_name()
            obj.name = name
        self.objects[name] = obj
        obj.init()

    def remove(self, name):
        self.objects[name].destroy()
        del self.objects[name]

    def create(self, class_name, name, x, y, **kwargs):
        if name is None or name=="":
            name = self._auto_name()
        obj = self.classes[class_name](self.scene, name, x, y, **kwargs)
        self.objects[name] = obj
        obj.init()
        return obj

    def bulkCreate(self, toCreate):
        """toCreate is a list of tuples of the form (class_name, name, x, y, kwargs)"""
        newObjects = []

        for class_name, name, x, y, kwargs in toCreate:
            if name is None or name=="":
                name = self._auto_name()
            obj = self.classes[class_name](self.scene, name, x, y, **kwargs)
            self.objects[name] = obj
            newObjects.append(obj)

        # Done in two steps because objects need to be available for other objects to subscribe to them
        for obj in newObjects:
            obj.init()

    def createFromTMX(self, tmx):
        # TODO: Import game objects from TMX object layer
        pass

    def clear(self):
        for obj in self.objects.values():
            obj.destroy()
        self.objects = {}

    def update(self, td):
        for obj in self.early_update:
            obj.update(td)

        for obj in self.normal_update:
            obj.update(td)

        for obj in self.late_update:
            obj.update(td)

    def draw(self, surface, camera_x, camera_y):
        # Updates sprites rects relative to camera
        self.visible.update(camera_x, camera_y)
        self.visible.draw(surface)

    def debug_draw(self, surface, camera_x, camera_y):
        for obj in self.objects.values():
            obj.debug_draw(surface, camera_x, camera_y)
