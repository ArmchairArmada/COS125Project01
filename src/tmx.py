#!/usr/bin/env python

"""
Custom TMX loading module.  This will implement only the features that are needed and they will be custom tailored
for our purposes.


NOTES:
Maybe it can be converted into a format like this:

[
    {
        "tag":"type",
        "param":"value",
        "text":"Inner contents of tag",
        "children":[
            "tag":"type",
            "param":"value",
            "text":"Inner contents of tag",
            "children":[]
        ]
    }
]

Or maybe I can try to come up with something more TMX specific...
It should group similar types of data: layers, objects, etc.

Maybe all object groups should be collapsed into one set of objects, since I do not plan on having my object manager
handle multiple different object groups.

Tiles can have properties.  This should be used when generating the tile map's collision information: solid, painful,
deadly, water, slippery, slow, floor offsets, ceiling offsets, etc.
"""

from xml.etree import ElementTree
import base64    # Used for text encoding compressed tile map data  (Note: CSV seems a lot simpler)
import zlib      # Used for compressing tile map data

import assets

class TMX:
    def __init__(self, filename):
        self.load(filename)

    def load(self, filename):
        # Load in all the data
        tree = ElementTree.parse(assets.path(filename))
        root = tree.getroot()

        # TODO: Load everything into a more structured format with decompressed/decoded data (maybe dicts & lists)
