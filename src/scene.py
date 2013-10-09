#!/usr/bin/env python

"""
Scene where all the action takes place
"""

import tmxlib
import assets

class Scene:
    def __init__(self, state, filename):
        self.state = state
        # TODO: Create collision group
        # TODO: Create Object Manager

        # Load TMX file
        tmx = tmxlib.Map.open(assets.path(filename))

        # Initialize variables using TMX map properties
        # Properties used in maps are:
        #   name    - The name of the map
        #   script  - File name of custom script that should be used with map
        #   music   - The file name of the music that should play during the level

        self.width, self.height = tmx.pixel_size

        self.properties = tmx.properties
        self.name = tmx.properties.get("name", "")
        self.script = tmx.properties.get("script")
        self.music = tmx.properties.get("music", "music.ogg")

        # TODO: Generate tile map using TMX tile map data
        # TODO: Pass TMX object data to Object Manager to generate objects
        # TODO: Load script that may have been in TMX's map properties
        # TODO: Initialize script

    def switch_states(self, new_state, *args, **kwargs):
        self.state.switch(new_state, *args, **kwargs)

    def update(self, td):
        # TODO: Update object manager
        # TODO: Update player (maybe this will be done in object manager)
        # TODO: Update camera (maybe this will be done in object manager)
        pass

    def draw(self, surface):
        # TODO: Draw tile map back layer
        # TODO: Draw object manager
        # TODO: Draw tile map front layer
        pass
