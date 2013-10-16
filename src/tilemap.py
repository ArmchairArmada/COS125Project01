#!/usr/bin/env python

"""
Tile map layer

For simplicity sake maps will have the following limitations:

1 Tile Set per map

"""

import pygame
import assets

class Tile:
    def __init__(self, number, properties, image):
        self.number = number
        self.properties = properties
        self.image = image
        self.tile_height, self.tile_width = image.get_size()

        self.type = properties.get("type")
        self.left_height = float(properties.get("left_height", self.tile_height))
        self.right_height = float(properties.get("right_height", self.tile_height))
        self.slope = (self.right_height - self.left_height) / float(self.tile_width)

    def getHeight(self, x):
        return self.tile_height - self.slope * x - self.left_height


class TileSet:
    def __init__(self, tmx_tileset):
        self.name = tmx_tileset.name
        self.tile_width, self.tile_height = tmx_tileset.tile_size
        image_file = tmx_tileset.image.source
        self.tile_gfx = assets.getImageList(image_file, tmx_tileset.column_count, tmx_tileset.row_count, False)
        self.tiles = []
        for t in tmx_tileset:
            self.tiles.append(Tile(t.number, t.properties, self.tile_gfx[t.number]))


class TileLayer:
    def __init__(self, tilemap, tmx_layer):
        self.tilemap = tilemap
        self.name = tmx_layer.name
        self.visible = tmx_layer.visible
        self.opacity = tmx_layer.opacity
        self.properties = tmx_layer.properties
        self.parallax = float(self.properties.get("parallax", 1.0))
        self.tile_width = self.tilemap.tile_width
        self.tile_height = self.tilemap.tile_height

        self.image = pygame.Surface((tilemap.pixel_width, tilemap.pixel_height), pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.fill((0,0,0,0))

        self.data = {}

        w = self.tilemap.width
        tw = self.tile_width
        th = self.tile_height
        for i, d in enumerate(tmx_layer.data):
            y = (i / w)
            x = (i % w)
            tile = tilemap.tileset.tiles[d-1]
            self.data[(x,y)] = tile
            if d != 0:
                self.image.blit(tile.image, (x*tw, y*th))

    def draw(self, surface, x, y):
        if self.visible:
            surface.blit(self.image, (int(x * self.parallax), int(y * self.parallax)))

    def iterRect(self, x, y, width, height):
        tile_width = self.tilemap.tile_width
        tile_height = self.tilemap.tile_height
        start_x = int((x*self.parallax) / tile_width)
        start_y = int((y*self.parallax) / tile_height)
        end_x = int(((x+width)*self.parallax) / tile_width)
        end_y = int(((y+height)*self.parallax) / tile_height)
        for j in xrange(start_y, end_y+1):
            for i in xrange(start_x, end_x+1):
                tile = self.data.get((i,j))
                yield (tile, (i,j), (i*tile_width, j*tile_height))

    def getHeight(self, x, y, height):
        tile_y = y + height
        for tile, tile_pos, pixel_pos in self.iterRect(x, y, 1, height):
            if tile.type == "block":
                tile_y = min(tile_y, pixel_pos[1])
            elif tile.type == "slope":
                tile_y = min(tile_y, pixel_pos[1] + tile.getHeight(x - pixel_pos[0]))
        return tile_y


class TileMap:
    def __init__(self, tmx):
        self.width, self.height = tmx.size
        self.tile_width, self.tile_height = tmx.tile_size
        self.pixel_width, self.pixel_height = tmx.pixel_size

        self.tileset = TileSet(tmx.tilesets[0])

        self.background = None
        self.foreground = None

        self.layers = []
        for layer in tmx.layers:
            if layer.type == "tiles":
                tmp = TileLayer(self, layer)
                self.layers.append(tmp)
                if tmp.name == "Background":
                    self.background = tmp
                elif tmp.name == "Foreground":
                    self.foreground = tmp

    def draw(self, surface, x, y, start=0, end=999999999):
        for layer in self.layers[start:end]:
            layer.draw(surface, x, y)
