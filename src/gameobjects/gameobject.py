#!/usr/bin/env python

"""
The GameObject is the basis for all interactive objects in the game.

It needs an ObjectManager object to attaches and detaches itself from.
"""

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

    def addGameObject(self, obj):
        self.to_add.append(obj)

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
    def __init__(self, objectMgr, name, x, y):
        """GameObject base class which all other game objects will derive from."""
        global _object_id

        super(GameObject, self).__init__()

        self.x = x
        self.y = y

        self.name = name
        if name is None:
            self.name = str(_object_id)
            _object_id += 1

        self.objectMgr = objectMgr
        objectMgr.addGameObject(self)

    def update(self, td):
        """This will be overridden by child classes"""
        pass

    def draw(self, surface, x, y):
        """Draw object.  x and y are camera coordinates.  This will be overridden"""
        pass

    def destroy(self):
        self.objectMgr.removeGameObject(self)


if __name__ == "__main__":
    import testing
    import gameobjects

    testing.init()

    mgr = ObjectManager()
    img = gameobjects.Image(mgr, None, 10, 10, "test.png")

    def u(td):
        testing.display.fill((255, 255, 255))
        mgr.update(td)
        mgr.draw(testing.display, 0, 0)

    testing.loop(u)
