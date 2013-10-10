#!/usr/bin/env python

"""
Scene where all the action takes place.

To simplify things, all tile maps will have 3 layers:
    A background layer is drawn first
    Then an object layer is drawn
    And a foreground layer that is drawn on top of everything
"""

import tmxlib
import assets
import tilemap
import objectmgr

class Scene:
    def __init__(self, state, filename):
        self.state = state
        # TODO: Create Object Manager
        self.object_mgr = objectmgr.ObjectManager(self)

        # Load TMX file
        tmx = tmxlib.Map.open(assets.path(filename))

        # Initialize variables using TMX map properties
        # Properties used in maps are:
        #   name          - The name of the map
        #   script        - File name of custom script that should be used with map
        #   music         - The file name of the music that should play during the level
        #   camera_x      - Camera's starting x coordinate
        #   camera_y      - Camera's starting y coordinate
        #   camera_state  - State camera should start in
        #   camera_params - Parameters to initialize camera's state in dict format

        self.width, self.height = tmx.pixel_size

        self.properties = tmx.properties
        self.name = tmx.properties.get("name", "")
        self.script = tmx.properties.get("script")
        self.music = tmx.properties.get("music", "music.ogg")

        # Camera initialization properties
        # TODO: Create real camera object
        self.camera = lambda:None

        # TODO: Pass these to an actual Camera object
        self.camera.x = int(tmx.properties.get("camera_x", 0))
        self.camera.y = int(tmx.properties.get("camera_y", 0))
        # TODO: Camera state (normal, follow, move to, etc.)
        # TODO: Camera state parameters

        # Generate tile map using TMX tile map data
        self.tilemap = tilemap.TileMap(tmx)

        # TODO: Pass TMX object data to Object Manager to generate objects
        # TODO: Load script that may have been in TMX's map properties
        # TODO: Initialize script

    def switch_states(self, new_state, *args, **kwargs):
        self.state.switch(new_state, *args, **kwargs)

    def update(self, td):
        # TODO: Update object manager
        self.object_mgr.update(td)
        # TODO: Update player (maybe this will be done in object manager)
        # TODO: Update camera (maybe this will be done in object manager)
        pass

    def draw(self, surface):
        # Draw tile map back layer
        self.tilemap.draw(surface, -self.camera.x, -self.camera.y, 0, 1)
        # Draw object manager
        self.object_mgr.draw(surface)
        # Draw tile map front layer
        self.tilemap.draw(surface, -self.camera.x, -self.camera.y, 1, 2)
