#!/usr/bin/env python

"""
Base GameObject
"""

class GameObject(object):
    def __init__(self, scene, name, x, y, **kwargs):
        super(GameObject, self).__init__()
        self.scene = scene
        self.obj_mgr = scene.object_mgr
        self.name = name
        self.x = x
        self.y = y

    def init(self):
        """Initiation code.  Override as needed."""
        pass

    def kill(self):
        self.scene.object_mgr.remove(self.name)

    def destroy(self):
        """Clean up code.  Override as needed"""
        pass

    def update(self, td):
        pass

    def debug_draw(self, surface):
        pass
