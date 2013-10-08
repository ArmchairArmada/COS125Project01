#!/usr/bin/env python

"""
Scene where all the action takes place
"""

class Scene:
    def __init__(self, state, filename):
        self.state = state
        # TODO: Create collision group
        # TODO: Create Object Manager
        # TODO: Load TMX file
        # TODO: Initialize variables using TMX map properties
        # TODO: Generate tile map using TMX tile map data
        # TODO: Pass TMX object data to Object Manager to generate objects
        # TODO: Load script that may have been in TMX's map properties
        # TODO: Initialize script
        pass

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
