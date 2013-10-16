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

    def iterHeights(self, x, y):
        #step = self.width / ((self.width / self.tile_layer.tile_width) + 1)
        #print step
        for i in xrange(0, self.width, self.tile_layer.tile_width):
            yield self.tile_layer.getHeight(x + i, y, self.height)
        yield self.tile_layer.getHeight(x + self.width-2, y, self.height)

    def move(self, dest_x, dest_y):
        """Try to move gameobject to (dest_x, dest_y) with it colliding with solid blocks and slopes"""
        dx = dest_x - self.gameobject.x
        dy = dest_y - self.gameobject.y
        obj_y = self.gameobject.y + self.offset_y
        dest_x = dest_x + self.offset_x
        dest_y = dest_y + self.offset_y
        move_x = dest_x
        move_y = dest_y
        horizontal_collide = False
        vertical_collide = False

        was_on_ground = self.on_ground

        # TODO: Tile collision callback function

        # Check horizontal collisions
        box_height = self.height - self.step_height

        for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(dest_x, obj_y, self.width-1, box_height):
            type = tile.properties.get("type")
            if type == "block":
                if dx > 0:
                    move_x = min(move_x, pixel_pos[0] - self.width)
                    horizontal_collide = True
                elif dx < 0:
                    move_x = max(move_x, pixel_pos[0] + self.tile_layer.tile_width)
                    horizontal_collide = True

        self.on_ground = False
        if dy < 0:
            for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(move_x, dest_y, self.width-1, box_height):
                type = tile.properties.get("type")
                if type == "block":
                    move_y = max(move_y, pixel_pos[1] + self.tile_layer.tile_height)
                    vertical_collide = True

        else:
            move_y = min(self.iterHeights(move_x, dest_y)) - self.height
            if move_y < dest_y-0.5:
                self.on_ground = True

        # For some reason the object drops down a little when going off ledges.  This might be a hack.
        if was_on_ground and not self.on_ground:
            move_y -= self.step_height

        if self.on_ground:
            vertical_collide = True
            move_y = math.ceil(move_y)

        self.gameobject.x = move_x - self.offset_x
        self.gameobject.y = move_y - self.offset_y

        return (horizontal_collide, vertical_collide)

    def debug_draw(self, surface, camera_x, camera_y):
        import pygame
        pygame.draw.rect(surface, (0,0,255), (self.gameobject.x + self.offset_x + camera_x, self.gameobject.y + self.offset_y + camera_y, self.width, self.height), 1)
        if self.on_ground:
            pygame.draw.circle(surface, (0,0,255), (int(self.gameobject.x + self.offset_x + camera_x + self.width/2), int(self.gameobject.y + self.offset_y + camera_y + self.height)), 3)
        for i,h in enumerate(self.iterHeights(self.gameobject.x + self.offset_x, self.gameobject.y + self.offset_y)):
            pygame.draw.circle(surface, (0,128,255), (int(self.gameobject.x + self.offset_x + i * 16 + camera_x), int(h + camera_y)), 3)
