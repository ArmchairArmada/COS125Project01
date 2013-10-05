#!/usr/bin/env python

"""
Assets for the game, like graphics, sounds, fonts, and animations
"""

import os
import pygame
import animation

# Dictionary for storing cached copies of files
_images = {}
_image_lists = {}
_sounds = {}
_fonts = {}
_animations = {}

_data_py = os.getcwd()
_data_dir = os.path.normpath(os.path.join(_data_py, "../", "data"))

def path(filename):
    # Returns a path to a file in the data directory
    return os.path.join(_data_dir, filename)

def load(filename, mode="rt"):
    # Opens a file in the data directory
    return open(os.path.join(_data_dir, filename), mode)

def getImageList(filename, columns, rows):
    """Splits an image by rows and columns and puts those sub-images into a list to be returned."""
    img_list = _image_lists.get(filename)
    if img_list:
        return img_list
    image = getImage(filename)
    width = image.get_width() / columns
    height = image.get_height() / rows
    img_list = []
    for y in xrange(rows):
        for x in xrange(columns):
            subImg = image.subsurface(pygame.Rect(x * width, y * height, width, height))
            img_list.append(subImg)
    _image_lists[filename] = img_list
    return img_list

def getImage(filename):
    """Loads an image if it is not already loaded, else return the copy we have"""
    tmp = _images.get(filename)
    if tmp:
        return tmp
    tmp = pygame.image.load(path(filename)).convert_alpha()
    _images[filename] = tmp
    return tmp

def getSpriteAnim(filename):
    """Loads an animation from file or returns a cached copy"""
    tmp = _animations.get(filename)
    if tmp:
        return tmp
    tmp = animation.Animation()
    tmp.loadSpriteAnim(path(filename))
    _animations[filename] = tmp
    return tmp

def getSound(filename):
    """Loads a sound file or returns a cached copy"""
    tmp = _sounds.get(filename)
    if tmp:
        return tmp
    tmp = pygame.mixer.Sound(path(filename))
    _sounds[filename] = tmp
    return tmp

def getFont(filename, size):
    """Loads a font or returns a cached copy"""
    key = (filename,size)
    tmp = _fonts.get(key)
    if tmp:
        return tmp
    tmp = pygame.font.Font(path(filename), size)
    _fonts[key] = tmp
    return tmp



if __name__ == "__main__":
    """Running this file directly will perform tests to see if everything loads correctly"""
    import testing
    testing.init()

    img = getImage("test.png")
    print "Loaded Image: test.png", img, _images["test.png"], img.get_width(), img.get_height()

    snd = getSound("test.wav")
    print "Loaded Sound: test.wav", snd, _sounds["test.wav"]
    snd.play()

    anim = getSpriteAnim("test_anim.json")
    print "Loaded Animation:", anim, _animations["test_anim.json"]

    cursor = animation.SimpleCursor()
    cursor.play(anim)

    fadeAnim = animation.Animation()
    fadeAnim.create(True, [((255,255,255), 1000), ((0,128,255), 1000)])

    fade = animation.InterpolatedCursor()
    fade.play(fadeAnim)

    font = getFont("test.ttf", 20)
    font_img = font.render("Test", True, (0,0,0))

    def u(td):
        fade.update(td)
        testing.display.fill((int(fade.frame[0]), int(fade.frame[1]), int(fade.frame[2])))
        testing.display.blit(img, (0,0))
        cursor.update(td)
        testing.display.blit(cursor.frame, (100,10))
        testing.display.blit(font_img, (10,50))

    testing.loop(u)
