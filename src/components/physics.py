#!/usr/bin/env python

class Physics:
    def __init__(self, gameobject, mapcollide, friction=0.7, air_resistance=0.0001, bounciness=0.0, gravity = 0.001):
        self.gameobject = gameobject
        self.mapcollide = mapcollide
        self.vx = 0.0
        self.vy = 0.0
        self.friction = friction
        self.air_resistance = air_resistance
        self.bounciness = bounciness
        self.gravity = gravity
        self.force_x = 0.0
        self.force_y = 0.0
        self.jumping = False

    def update(self, td):
        was_on_ground = self.mapcollide.on_ground

        if not self.jumping and was_on_ground:
            #self.setForceY(4.0 / (td+0.001))
            self.setForceY(8.0 / (td+0.001))

        self.vx += self.force_x * td
        self.vy += (self.force_y + self.gravity) * td

        x = self.gameobject.x + self.vx * td
        y = self.gameobject.y + self.vy * td

        h_collide, v_collide = self.mapcollide.move(x,y)

        if h_collide:
            self.vx = -self.vx * self.bounciness

        if v_collide:
            if self.mapcollide.on_ground:
                self.vx -= self.vx * self.friction * td
                self.jumping = False
            self.vy = -self.vy * self.bounciness

        if not h_collide and not v_collide:
            self.vx -= self.vx * self.air_resistance * td
            self.vy -= self.vy * self.air_resistance * td

        if not self.jumping and not self.mapcollide.on_ground and was_on_ground:
            self.setForceY(0.0)

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

    def jump(self, vy):
        self.jumping = True
        self.vy = vy

    def debug_draw(self, surface, camera_x, camera_y):
        import pygame
        pygame.draw.line(surface, (0, 255, 0), (self.gameobject.x + camera_x, self.gameobject.y + camera_y), (self.gameobject.x + self.vx * 100 + camera_x, self.gameobject.y + self.vy * 100 + camera_y))
