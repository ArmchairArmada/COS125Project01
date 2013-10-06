#!/usr/bin/env python

"""Game Objects"""

from gameobject import ObjectManager
from image import Image
from camera import Camera
from sound import Sound
from player import Player

_classes ={
    "Image": Image,
    "Camera": Camera,
    "Player": Player,
    "Sound": Sound
}

def create(className, scene, name, x, y, **kwargs):
    c = _classes.get(className)
    if c:
        return c(scene, name, x, y, **kwargs)
