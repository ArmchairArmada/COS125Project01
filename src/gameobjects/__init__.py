#!/usr/bin/env python

"""Game Objects"""

from gameobject import ObjectManager
from image import Image
from camera import Camera

_classes ={
    "Image": Image
}

def create(className, objMgr, name, x, y):
    c = _classes.get(className)
    if c:
        return c(objMgr, name, x, y)
