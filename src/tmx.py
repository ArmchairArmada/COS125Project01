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
#import base64    # Used for text encoding compressed tile map data  (Note: CSV seems a lot simpler)
#import zlib      # Used for compressing tile map data

import assets

def _attrib(node, key, defval):
    value = node.attrib.get(key)
    if value:
        return value
    return defval


def _properties(node):
    properties = {}
    for child in node:
        if child.tag == "property":
            properties[child.attrib["name"]] = child.attrib["value"]
    return properties


class TileSet:
    def __init__(self, node):
        self.firstgid = int(_attrib(node, "firstgid", 1))
        self.source = _attrib(node, "source", "")
        self.name = _attrib(node, "name", "unnamed")
        self.tilewidth = int(_attrib(node, "tilewidth", 16))
        self.tileheight = int(_attrib(node, "tilewidth", 16))
        self.spacing = int(_attrib(node, "spacing", 0))
        self.margin = int(_attrib(node, "margin", 0))

        self.tiles = {}

        for child in node:
            if child.tag == "image":
                self.image_source = _attrib(child, "source", "")
                self.image_width = _attrib(child, "width", 256)
                self.image_height = _attrib(child, "height", 256)

            elif child.tag == "tile":
                # Going to ignore terrain and probability
                prop_node = child.find("properties")
                self.tiles[_attrib(child, "id", 0)] = _properties(prop_node)

            else:
                print "Unhandled TileSet Tag: " + child.tag


class Layer:
    def __init__(self, node):
        self.name = _attrib(node, "name", "unnamed")
        self.x = int(_attrib(node, "x", 0))
        self.y = int(_attrib(node, "y", 0))
        self.width = int(_attrib((node, "width", 100)))
        self.height = int(_attrib(node, "height", 100))
        self.opacity = float(_attrib(node, "opacity", "1"))
        self.visible = _attrib(node, "visible", "1") == "1"

        


class TMX:
    def __init__(self, filename):
        self.version = "0.0"
        self.width = 0
        self.height = 0
        self.orientation = ""
        self.tile_height = 0
        self.tile_width = 0

        self.properties = {}
        self.tilesets = []
        self.layers = []
        self.objectgroups = []

        self.load(filename)

    def load(self, filename):
        # Load in all the data
        tree = ElementTree.parse(assets.path(filename))
        root = tree.getroot()

        self._parse(root)

    def _parse(self, node):
        func_name = "_tag_"+node.tag
        if hasattr(self, func_name):
            getattr(self, func_name)(node)

        for child in node:
            self._parse(child)

    def _tag_map(self, node):
        self.version = _attrib(node, "version", "0.0")
        self.width = int(_attrib(node, "width", 100))
        self.height = int(_attrib(node, "height", 100))
        self.orientation = _attrib(node, "orientation", "orthogonal")
        self.tile_height = int(_attrib(node, "tileheight", 16))
        self.tile_width = int(_attrib(node, "tilewidth", 16))

        prop_node = node.find("properties")
        self.properties = _properties(prop_node)

    def _tag_tileset(self, node):
        self.tilesets.append(TileSet(node))

    def _tag_layer(self):
        self.layers.append(Layer(node))
