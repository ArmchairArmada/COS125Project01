#!/usr/bin/env python

"""
This is just a scratchpad for testing little things
"""

import tmxlib
import assets
import pygame
import tilemap

d = pygame.display.set_mode((640,480))

m = tmxlib.Map.open(assets.path("testing/tile_test.tmx"))
t = tilemap.TileMap(m)

y=0
x=0

p = True
while p:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            p = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                y -= 16
            if e.key == pygame.K_UP:
                y += 16
            if e.key == pygame.K_LEFT:
                x += 16
            if e.key == pygame.K_RIGHT:
                x -= 16

    x -= 0.05
    d.fill((2,5,10))
    t.draw(d, x, y)
    pygame.display.flip()

pygame.quit()
