#!/usr/bin/env python

"""
Tests for collisions between a rectangular region and a tilemap layer.
"""

import math


class MapCollider:
    def __init__(self, gameobject, tile_layer, offset_x, offset_y, width, height):
        self.gameobject = gameobject
        self.tile_layer = tile_layer
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height
        self.step_height = 8
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

        # Check horizontal collisions
        for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(dest_x, obj_y, self.width-1, self.height-1 - self.step_height):
            type = tile.properties.get("type")
            if type == "block":
                if dx > 0:
                    move_x = min(move_x, pixel_pos[0] - self.width)
                elif dx < 0:
                    move_x = max(move_x, pixel_pos[0] + self.tile_layer.tile_width)

            elif type == "slope":
                # TODO: Either block or step depending on slope height relative to y
                pass

            else:
                # TODO: Call tile collision callback
                pass

        # Check vertical collisions
        slope_move_y = move_y
        on_slope = False
        self.on_ground = False
        for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(move_x, dest_y, self.width-1, self.height-1):
            type = tile.type
            if type == "block":
                if dy > 0:
                    move_y = min(move_y, pixel_pos[1] - self.height)
                    self.on_ground = True
                elif dy < 0:
                    move_y = max(move_y, pixel_pos[1] + self.tile_layer.tile_height)

            elif type == "slope":
                # TODO: Collide with slopes
                if dy >= 0:
                    slope_x = move_x - pixel_pos[0] + self.width / 2
                    if 0 < slope_x < self.tile_layer.tile_width:
                        on_slope = True
                        slope_y = tile.slope * slope_x + (pixel_pos[1] + self.tile_layer.tile_height - tile.left_height)
                        slope_move_y = min(slope_move_y, slope_y - self.height)
                        self.on_ground = True

            else:
                # TODO: Call tile collision callback
                pass

        if on_slope:
            move_y = slope_move_y

        if self.on_ground:
            move_y = math.ceil(move_y)

        self.gameobject.x = move_x - self.offset_x
        self.gameobject.y = move_y - self.offset_y

    def debug_draw(self, surface, camera_x, camera_y):
        import pygame
        pygame.draw.rect(surface, (0,0,255), (self.gameobject.x + self.offset_x + camera_x, self.gameobject.y + self.offset_y + camera_y, self.width, self.height), 1)
