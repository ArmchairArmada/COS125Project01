#!/usr/bin/env python

"""
Player object.  The player will be controlling this and having him run and jump around.
"""

from gameobject import GameObject
import components
import assets
import inputs

ANIM_RUN = 0
ANIM_STAND = 1
ANIM_JUMP = 2
ANIM_HURT = 3
ANIM_DIE = 4

STATE_ALIVE = 0
STATE_HURT = 1
STATE_DEAD = 2

LEFT = 0
RIGHT = 1

class Player(GameObject):
    def __init__(self, scene, name, x, y, **kwargs):
        super(Player, self).__init__(scene, name, x, y, **kwargs)
        self.sprite = components.AnimSprite(self, assets.getSpriteAnim("graphics/player.json"), "stand_r", -16, -16)
        self.mapcollide = components.MapCollider(self, scene.tilemap.foreground, -5, -9, 11, 24)
        self.physics = components.Physics(self, self.mapcollide, 0.03)
        self.health = components.Health(self)

        self.sound_hurt = assets.getSound("sounds/hurt.wav")
        self.sound_die = assets.getSound("sounds/die.wav")
        self.sound_land = assets.getSound("sounds/land.wav")

        self.state = STATE_ALIVE
        self.anim_state = ANIM_STAND
        self.run_accel = 0.004
        self.air_accel = 0.00025
        self.max_air_speed = 0.2
        self.facing = RIGHT
        self.jump_timer = 0
        self.max_jump_timer = 150
        self.jump_speed = -0.17
        self.jump_thrust = -0.002
        self.hurt_timer = 0
        self.max_hurt_timer = 300

    def init(self):
        self.scene.object_mgr.late_update.append(self)

    def destroy(self):
        self.sprite.destroy()
        self.scene.object_mgr.late_update.remove(self)

    def update(self, td):
        self.health.update()

        if self.state == STATE_ALIVE:
            self.hurt_timer -= td
            self.updateControls(td)

        was_on_ground = self.mapcollide.on_ground

        self.physics.update(td)

        if not was_on_ground and self.mapcollide.on_ground:
            self.sound_land.play()

        if self.state == STATE_ALIVE:
            for tile, tile_pos, pixel_pos in self.mapcollide.iterTiles():
                self.processTile(td, tile, tile_pos, pixel_pos)

        if self.state == STATE_DEAD:
            if not self.sprite.cursor.playing:
                self.kill()

        self.updateAnim(td)

    def updateControls(self, td):
        if self.mapcollide.on_ground:
            self.physics.applyForce(inputs.getHorizontal() * self.run_accel * td, 0)

            if inputs.getJumpPress():
                self.physics.jump(self.jump_speed)
                self.jump_timer = self.max_jump_timer

        else:
            if inputs.getHorizontal() < 0.0 and self.physics.vx > -self.max_air_speed or inputs.getHorizontal() > 0.0 and self.physics.vx < self.max_air_speed:
                self.physics.applyForce(inputs.getHorizontal() * self.air_accel * td, 0)

            self.jump_timer -= td
            if inputs.getJump() and self.jump_timer >= 0.0:
                self.physics.applyForce(0, self.jump_thrust * td)

    def processTile(self, td, tile, tile_pos, pixel_pos):
        if tile is not None:
            if tile.type == "spike":
                # TODO: Touch spike
                if not self.health.was_hurt:
                    self.hurt(-10)
            elif tile.type == "lava":
                # TODO: Touch lava
                if not self.health.was_hurt:
                    self.hurt(-10)

    def updateAnim(self, td):
        if self.anim_state == ANIM_HURT:
            if not self.sprite.cursor.playing:
                self.state = STATE_ALIVE
                self.anim_state = ANIM_STAND
                if self.facing == LEFT:
                    self.sprite.play("stand_l")
                else:
                    self.sprite.play("stand_r")

        elif self.anim_state != ANIM_DIE:
            if self.mapcollide.on_ground and not self.physics.jumping:
                if self.anim_state == ANIM_STAND:
                    if inputs.getHorizontal() < -0.01:
                        self.anim_state = ANIM_RUN
                        self.facing = LEFT
                        self.sprite.play("run_l")

                    if inputs.getHorizontal() > 0.01:
                        self.anim_state = ANIM_RUN
                        self.facing = RIGHT
                        self.sprite.play("run_r")

                elif self.anim_state == ANIM_RUN:
                    if abs(inputs.getHorizontal()) <= 0.01:
                        self.anim_state = ANIM_STAND
                        if self.facing == LEFT:
                            self.sprite.play("stand_l")
                        else:
                            self.sprite.play("stand_r")

                    if self.facing == RIGHT and inputs.getHorizontal() < -0.01:
                        self.facing = LEFT
                        self.sprite.play("run_l")

                    if self.facing == LEFT and inputs.getHorizontal() > 0.01:
                        self.facing = RIGHT
                        self.sprite.play("run_r")

                elif self.anim_state == ANIM_JUMP:
                    if self.mapcollide.on_ground:
                        self.anim_state = ANIM_STAND
                        if self.facing == LEFT:
                            self.sprite.play("stand_l")
                        else:
                            self.sprite.play("stand_r")
                else:
                    pass

            else:
                if self.anim_state != ANIM_JUMP:
                    self.anim_state = ANIM_JUMP
                    if self.facing == LEFT:
                        self.sprite.play("jump_l")
                    else:
                        self.sprite.play("jump_r")

        self.sprite.updateAnim(td)

    def hurt(self, amount):
        if self.hurt_timer < 0:
            self.sound_hurt.play()
            self.hurt_timer = self.max_hurt_timer
            self.anim_state = ANIM_HURT
            if self.facing == LEFT:
                self.sprite.play("hurt_l")
            else:
                self.sprite.play("hurt_r")
            self.health.change(amount)

    def die(self):
        self.sound_die.play()
        self.state = STATE_DEAD
        self.anim_state = ANIM_DIE
        if self.facing == LEFT:
            self.sprite.play("die_l")
        else:
            self.sprite.play("die_r")

    def zeroHealth(self):
        """ Called by Health component when health reaches 0 """
        print "Dead"
        self.die()

    def fullHealth(self):
        """ Called by Health component when health reaches maximum amount """
        print "Healed"

    def debug_draw(self, surface, camera_x, camera_y):
        super(Player, self).debug_draw(surface, camera_x, camera_y)
        self.sprite.debug_draw(surface, camera_x, camera_x)
        self.mapcollide.debug_draw(surface, camera_x, camera_y)
        self.physics.debug_draw(surface, camera_x, camera_y)
        self.health.debug_draw(surface, camera_x, camera_y)
