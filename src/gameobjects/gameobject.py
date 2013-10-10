#!/usr/bin/env python

"""
Base GameObject
"""

class GameObject(object):
    def __init__(self, scene, name, x, y, **kwargs):
        super(GameObject, self).__init__()
        self.scene = scene
        self.name = name
        self.x = x
        self.y = y

    def init(self):
        """Any init code that might modify a container should go here"""
        pass

    def destroy(self):
        pass

    def kill(self):
        self.scene.object_mgr.remove(self.name)

    def update(self, td):
        pass

    def debug_draw(self, surface):
        pass
