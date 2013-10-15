#!/usr/bin/env python

"""
Tests for collisions between a rectangular region and a tilemap layer.
"""

class MapCollider:
    def __init__(self, gameobject, tile_layer, offset_x, offset_y, width, height, step_height):
        self.gameobject = gameobject
        self.tile_layer = tile_layer
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height
        self.step_height = step_height
        self.on_ground = False

    def move(self, dest_x, dest_y):
        """Try to move gameobject to (dest_x, dest_y) with it colliding with solid blocks and slopes"""
        dx = dest_x - self.gameobject.x
        dy = dest_y - self.gameobject.y
        obj_y = self.gameobject.y + self.offset_y
        dest_x = dest_x + self.offset_x
        dest_y = dest_y + self.offset_y
        move_x = dest_x
        move_y = dest_y

        # TODO: Tile collision callback function

        for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(dest_x, obj_y, self.width-1, self.height-1):
            type = tile.properties.get("type")
            if type == "block":
                if dx > 0:
                    move_x = min(move_x, pixel_pos[0] - self.width)
                elif dx < 0:
                    move_x = max(move_x, pixel_pos[0] + self.tile_layer.tile_width)

            elif type == "slope":
                # TODO: Either block or step depending on slope height relative to y
                pass

        self.on_ground = False
        for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(move_x, dest_y, self.width-1, self.height-1):
            type = tile.properties.get("type")
            if type == "block":
                if dy > 0:
                    move_y = min(move_y, pixel_pos[1] - self.height)
                    self.on_ground = True
                elif dy < 0:
                    move_y = max(move_y, pixel_pos[1] + self.tile_layer.tile_height)

            elif type == "slope":
                # TODO: Collide with slopes
                pass

        self.gameobject.x = move_x - self.offset_x
        self.gameobject.y = move_y - self.offset_y
