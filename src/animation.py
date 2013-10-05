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


class Cursor(object):
    """Keeps track of animation playback"""
    def __init__(self):
        super(Cursor, self).__init__()

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
        """Please overload with correct playback function"""
        return False


class SimpleCursor(Cursor):
    """Keeps track of animation playback"""
    def __init__(self):
        super(SimpleCursor, self).__init__()

    def update(self, td):
        """Non-interpolated animation cursor.  It puts current frame in self.frame."""
        self.time_to_next -= td
        if self.playing and self.time_to_next <= 0:
            self.frame_number += 1
            if self.frame_number >= len(self.animation.frames):
                if self.animation.looping:
                    self.frame_number = 0
                else:
                    self.frame_number = len(self.animation.frames) - 1
                    self.playing = False

            self.frame, t = self.animation.frames[self.frame_number]
            self.time_to_next += t
        return self.playing


class InterpolatedCursor(Cursor):
    def __init__(self):
        super(InterpolatedCursor, self).__init__()
        self.current_frame = None
        self.next_frame = None
        self.frame_delay = 0.0

    def play(self, animation):
        super(InterpolatedCursor, self).play(animation)
        self.current_frame = self.frame
        self.next_frame = animation.frames[1 % len(animation.frames)][0]
        self.frame_delay = float(self.time_to_next)

    def update(self, td):
        """Animates with interpolating values.  Good for paths."""
        self.time_to_next -= td
        if self.playing and self.time_to_next <= 0:
            self.frame_number += 1
            if self.frame_number >= len(self.animation.frames):
                if self.animation.looping:
                    self.frame_number = 0
                else:
                    self.frame_number = len(self.animation.frames) - 1
                    self.playing = False

            self.current_frame, t = self.animation.frames[self.frame_number]
            self.time_to_next += t
            self.frame_delay = float(t)
            self.next_frame = self.animation.frames[(self.frame_number + 1) % len(self.animation.frames)][0]

        interpolation = self.time_to_next / self.frame_delay
        self.frame = [self.current_frame[i] * interpolation + self.next_frame[i] * (1.0 - interpolation) for i in xrange(len(self.current_frame))]

        return self.playing
