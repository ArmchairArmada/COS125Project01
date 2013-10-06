#!/usr/bin/env python

"""Game Objects"""

from gameobject import ObjectManager
from image import Image
from camera import Camera

_classes ={
    "Image": Image
}

def create(className, scene, name, x, y, **kwargs):
    c = _classes.get(className)
    if c:
        return c(scene, name, x, y, **kwargs)
