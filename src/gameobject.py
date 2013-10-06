#!/usr/bin/env python

"""
The GameObject is the basis for all interactive objects in the game.  It is a container for game object components
and it can handle messaging.

It needs an ObjectManager object to attaches and detaches itself from.
"""

import comfactory
import assets

_object_id = 0

class ObjectManager:
    def __init__(self):
        self.game_objects = {}
        self.to_add = []
        self.to_remove = []

    def _addGameObjects(self):
        for obj in self.to_remove:
            if obj.name in self.game_objects:
                del self.game_objects[obj.name]
        self.to_remove = []

    def _removeGameObjects(self):
        for obj in self.to_add:
            self.game_objects[obj.name] = obj
        self.to_add = []

    def createGameObject(self, name=None, x = 0.0, y = 0.0, comFile = None, comConfig=None):
        if comFile is not None:
            comConfig = assets.getData(comFile)
        obj = GameObject(self, name, x, y, comConfig)
        self.to_add.append(obj)
        return obj

    def removeGameObject(self, obj):
        self.to_remove.append(obj)

    def get(self, name):
        return self.game_objects.get(name)

    def update(self, td):
        self._addGameObjects()
        self._removeGameObjects()

        for obj in self.game_objects.itervalues():
            obj.update(td)

    def draw(self, surface, x, y):
        for obj in self.game_objects.itervalues():
            obj.draw(surface, x, y)


class GameObject(object):
    def __init__(self, objectMgr, name = None, x = 0.0, y = 0.0, comConfig = None):
        """Game objects are containers for components that can be updated and drawn.  comConfig is used to
        configure components used by the game object."""
        global _object_id

        super(GameObject, self).__init__()

        self.x = x
        self.y = y

        self.name = name
        if name is None:
            self.name = str(_object_id)
            _object_id += 1

        self.objectMgr = objectMgr

        self.components = {}
        self.updatable_components = []
        self.drawable_components = []

        if comConfig:
            self.configureComponents(comConfig)

    def configureComponents(self, comConfig):
        """comConfig is a list of lists describing components and their parameters.  A factory is used to generate
        the needed components and configure them."""
        for comClass, comName, kwargs in comConfig:
            self.components[comName] = comfactory.create(comClass, self, **kwargs)

    def update(self, td):
        for component in self.updatable_components:
            if component.enabled:
                component.update(td)

        for component in self.updatable_components:
            if component.enabled:
                component.lateUpdate(td)

    def draw(self, surface, x, y):
        """Draw all components.  x and y are camera coordinates."""
        for component in self.drawable_components:
            if component.visible:
                component.draw(surface, x, y)

    def addComponent(self, name, component):
        self.components[name] = component

    def getComponent(self, name):
        return self.components.get(name)

    def destroy(self):
        for component in self.components.iteritems():
            component.destroy()
        self.objectMgr.removeGameObject(self)


if __name__ == "__main__":
    import testing
    import assets

    testing.init()

    om = ObjectManager()
    o = om.createGameObject(None, 10, 10, "test_com_conf.json")

    def u(td):
        testing.display.fill((255,255,255))
        om.update(td)
        om.draw(testing.display, 0, 0)

    testing.loop(u)
