#!/usr/bin/env python

"""
The GameObject is the basis for all interactive objects in the game.  It is a container for game object components
and it can handle messaging.

It needs an ObjectManager object to attaches and detaches itself from.
"""

class GameObject(object):
    def __init__(self, objectMgr):
        super(GameObject, self).__init__()
        self.objectMgr = objectMgr
        objectMgr.addGameObject(self)

        self.components = {}
        self.updatable_components = []
        self.drawable_components = []

    def update(self, td):
        for component in self.updatable_components:
            component.update(td)

    def draw(self, td):
        for component in self.drawable_components:
            component.draw(td)

    def addComponent(self, name, component):
        self.components[name] = component

    def getComponent(self, name):
        return self.components.get(name)

    def destroy(self):
        for component in self.components.iteritems():
            component.destroy()
        self.objectMgr.removeGameObject(self)
