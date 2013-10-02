#!/usr/bin/env python

"""Animation file format, right now, is a text file that looks like this:
{"image":"filename.png",
"columns":8,
"rows":8,
"looping":true,
frames:[
    (frame #, duration),
    ...
]
}"""

import json
import assets

class Animation:
    """Describes an animation sequence"""
    def __init__(self):
        # TODO: Load animation from file
        self.looping = False
        self.frames = []

    def create(self, looping=False, frames=[]):
        self.looping = looping
        self.frames = frames

    def loadSpriteAnim(self, filename):
        """Loads sprite animation from file."""
        self.frames = []
        file = assets.load(filename)
        tmp = json.load(file)
        file.close()

        self.looping = tmp["looping"]

        img_list = assets.getImageList(tmp["image"], tmp["columns"], tmp["rows"])
        for cell,duration in tmp["frames"]:
            self.frames.append((img_list[cell], duration))

class Cursor:
    """Keeps track of animation playback"""
    def __init__(self):
        self.animation = None
        self.frame_number = 0
        self.time_to_next = 0
        self.frame = None
        self.playing = True

    def play(self, animation):
        self.animation = animation
        self.frame_number = 0
        self.time_to_next = animation.frames[0][1]
        self.frame = animation.frames[0][0]
        self.playing = True

    def update(self, td):
        self.time_to_next -= td
        if self.playing and self.time_to_next <= 0:
            self.frame_number += 1
            if self.frame_number >= len(self.animation.frames):
                if self.animation.looping:
                    self.frame_number = 0
                else:
                    self.frame_number = len(self.animation.frames) - 1
                    self.playing = False

            self.frame, self.time_to_next = self.animation.frames[self.frame_number]
        return self.playing
