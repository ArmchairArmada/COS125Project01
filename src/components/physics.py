#!/usr/bin/env python

class Physics:
    def __init__(self, gameobject, mapcollide, friction=0.7, bounciness=0.0, gravity = 0.001):
        self.gameobject = gameobject
        self.mapcollide = mapcollide
        self.vx = 0.0
        self.vy = 0.0
        self.friction = friction
        self.bounciness = bounciness
        self.gravity = gravity
        self.force_x = 0.0
        self.force_y = 0.0

    def update(self, td):
        self.vx += self.force_x * td
        self.vy += (self.force_y + self.gravity) * td

        x = self.gameobject.x + self.vx * td
        y = self.gameobject.y + self.vy * td

        h_collide, v_collide = self.mapcollide.move(x,y)

        if h_collide:
            self.vx = -self.vx * self.bounciness

        if v_collide:
            if self.vy > 0:
                self.vx -= self.vx * self.friction
            self.vy = -self.vy * self.bounciness

    def applyForce(self, x, y):
        self.vx += x
        self.vy += y

    def setForce(self, x, y):
        self.vx = x
        self.vy = y

    def setForceX(self, x):
        self.vx = x

    def setForceY(self, y):
        self.vy = y

    def debug_draw(self, surface, camera_x, camera_y):
        import pygame
        pygame.draw.line(surface, (0, 255, 0), (self.gameobject.x + camera_y, self.gameobject.y + camera_y), (self.gameobject.x + self.vx + camera_x, self.gameobject.y + self.vy + camera_y))
