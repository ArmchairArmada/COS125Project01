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

    def getHeights(self, x, y):
        # Returns 3 collisions: left, center, and right
        left = self.tile_layer.getHeight(x, y, self.height)
        center = self.tile_layer.getHeight(x + self.width / 2.0, y, self.height)
        right = self.tile_layer.getHeight(x + self.width-1, y, self.height)
        return (left, center, right)

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
        #if self.on_ground:
        #    box_height = self.height - 1 - self.step_height
        #else:
        #    box_height = self.height - 2

        box_height = self.height - 1 - self.step_height

        for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(dest_x, obj_y, self.width-1, box_height):
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

        self.on_ground = False
        if dy < 0:
            for tile, tile_pos, pixel_pos in self.tile_layer.iterRect(move_x, dest_y, self.width-1, box_height):
                type = tile.properties.get("type")
                if type == "block":
                    move_y = max(move_y, pixel_pos[1] + self.tile_layer.tile_height)

        else:
            left, center, right = self.getHeights(move_x, dest_y)
            if center is not None:
                if move_y > center - self.height:
                    move_y = center - self.height
                    self.on_ground = True

            else:
                if left is not None and right is not None:
                    tmp = (left + right) / 2 - self.height
                    if move_y > tmp:
                        move_y = tmp
                        self.on_ground = True
                elif left is not None:
                    if move_y > left - self.height:
                        move_y = left - self.height
                        self.on_ground = True
                elif right is not None:
                    if move_y > right - self.height:
                        move_y = right - self.height
                        self.on_ground = True
                else:
                    pass

        if self.on_ground:
            move_y = math.ceil(move_y)

        self.gameobject.x = move_x - self.offset_x
        self.gameobject.y = move_y - self.offset_y

    def debug_draw(self, surface, camera_x, camera_y):
        import pygame
        pygame.draw.rect(surface, (0,0,255), (self.gameobject.x + self.offset_x + camera_x, self.gameobject.y + self.offset_y + camera_y, self.width, self.height), 1)
        if self.on_ground:
            pygame.draw.circle(surface, (0,0,255), (int(self.gameobject.x + self.offset_x + camera_x + self.width/2), int(self.gameobject.y + self.offset_y + camera_y + self.height)), 3)
