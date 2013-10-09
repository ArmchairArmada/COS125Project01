#!/usr/bin/env python

"""
This is just a scratchpad for testing little things
"""

import tmxlib
import assets

m = tmxlib.Map.open(assets.path("testing/tile_test.tmx"))
for o in m.layers[1].all_objects():
    print o.name, o.type, o.x, o.y, o.width, o.height, o.properties
