#!/usr/bin/env python

"""
Tile map layer

For simplicity sake maps will have the following limitations:

1 Tile Set per map

"""

import pygame
import assets

class TileSet:
    def __init__(self, tmx_tileset):
        self.name = tmx_tileset.name
        self.tile_width, self.tile_height = tmx_tileset.tile_size
        image_file = tmx_tileset.image.source
        self.tile_gfx = assets.getImageList(image_file, tmx_tileset.column_count, tmx_tileset.row_count, False)
        self.tile_properties = {}
        for t in tmx_tileset:
            self.tile_properties[t.number] = t.properties


class TileLayer:
    def __init__(self, tilemap, tmx_layer):
        self.tilemap = tilemap
        self.name = tmx_layer.name
        self.visible = tmx_layer.visible
        self.opacity = tmx_layer.opacity
        self.properties = tmx_layer.properties
        self.parallax = float(self.properties.get("parallax", 1.0))

        self.image = pygame.Surface((tilemap.pixel_width, tilemap.pixel_height), pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.fill((0,0,0,0))

        w = self.tilemap.width
        tw = self.tilemap.tile_width
        th = self.tilemap.tile_height
        for i, d in enumerate(tmx_layer.data):
            if d != 0:
                img = tilemap.tileset.tile_gfx[d-1]
                y = (i / w) * tw
                x = (i % w) * th
                self.image.blit(img, (x, y))

    def draw(self, surface, x, y):
        if self.visible:
            surface.blit(self.image, (int(x * self.parallax), int(y * self.parallax)))


class TileMap:
    def __init__(self, tmx):
        self.width, self.height = tmx.size
        self.tile_width, self.tile_height = tmx.tile_size
        self.pixel_width, self.pixel_height = tmx.pixel_size

        self.tileset = TileSet(tmx.tilesets[0])

        self.layers = []
        for layer in tmx.layers:
            if layer.type == "tiles":
                self.layers.append(TileLayer(self, layer))

    def draw(self, surface, x, y, start=0, end=999999999):
        for layer in self.layers[start:end]:
            layer.draw(surface, x, y)
