## File created by: Diego Ochoa

# The sprites module contains all the sprites
# Sprites include: player, mob - moving object


import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import Cooldown
#from utils import Spritesheet
from random import randint
from random import choice
from os import path
vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        #self.spritesheet = Spritesheet(path.join(self.game.img_folder, "spritesheet.png"))
        #self.load_images()
        self.image = pg.Surface((32, 32))
        self.image = game.player_img
        self.image.set_colorkey(BLACK)
        self.image_inv = game.player_img_inv
        self.rect = self.image.get_rect()
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        self.vel = vec(0,0)
        self.dir = vec(1,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.speed = 250
        self.health = 100
        self.coins = 0
        self.cd = Cooldown(1000)
        self.attack_cd = Cooldown(1000)  
        self.dir = vec(0,0)
        self.walking = False
        self.jump_power = 100
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
    def jump(self):
        #checks if something is one pixel below for jump
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y += -1
        if hits: 
            self.vel.y = -self.jump_power



    #def load_images(self):
        #self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                #self.spritesheet.get_image(0, 32, 32, 32)]
        #for frame in self.standing_frames:
            #frame.set_colorkey(BLACK)
        # self.walk_frames_r
        # self.walk_frames_l
        # pg.transform.flip

    #def animate(self):
        #now = pg.time.get_ticks()
        #if not self.jumping and not self.walking:
            #if now - self.last_update > 350:
                #print(now)
                #self.last_update = now
                #self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                #bottom = self.rect.bottom
                #self.image = self.standing_frames[self.current_frame]
                ##self.rect = self.image.get_rect()
                #self.rect.bottom = bottom
    def get_keys(self):
        self.vel = vec(0,GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.jump

        if keys[pg.K_k]:
            if self.attack_cd.ready():
                Attack(self.game, self.rect.x, self.rect.y, self.dir)
                self.attack_cd.start()
        if keys[pg.K_k]:
            print(self.rect.x)
            p = Attack(self.game, self.rect.x, self.rect.y, self.dir)
        if keys[pg.K_w]:
            #for sprite in self.game.all_sprites:
               # sprite.rect.x -= 25
            self.vel.y = -self.speed*self.game.dt
            self.dir = vec(0,-1)
        if keys[pg.K_a]:
            #for sprite in self.game.all_sprites:
                #sprite.rect.x += 25
            self.vel.x = -self.speed*self.game.dt
            self.dir = vec(-1,0)
        if keys[pg.K_s]:
            #for sprite in self.game.all_sprites:
                #sprite.rect.y -= 25
            self.vel.y = self.speed*self.game.dt
            self.dir = vec(0,1)
        if keys[pg.K_d]:
           # for sprite in self.game.all_sprites:
               # sprite.rect.y += 25
            self.vel.x = self.speed*self.game.dt
            self.dir = vec(1,0)
        # accounting for diagonal
        if self.vel[0] != 0 and self.vel[1] != 0:
            self.vel *= 0.7071
    
    #def effects_trail(self):
        #if self.effect_cd.ready():
            #EffectTrail(self.game, self.rect.x,self.rect.y)
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                print(self.pos)
                if self.vel.x > 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                        
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.x += self.vel.x
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                # hits[0].vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # print(self.pos)
                if self.vel.y > 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                        
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmovable":
                                self.pos.y = hits[1].rect.bottom
                    else:
                        self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                # hits[0].vel.x = 0
                self.rect.y = self.pos.y

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()
                # print("Ouch!")
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
                print(self.coins)

    def update(self):
        self.get_keys()
        #self.animate()
        #self.effects_trail()
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_coins, True)

          # Check if player is off-screen to switch map
        if self.rect.x < 0:
            self.rect.x = WIDTH - TILE_SIZE
            load_tilemap(level2.txt)

    #switches map
        if self.rect.left < 0:
            self.game.load_new_map("level2.txt")
            self.rect.right = WIDTH

        elif self.rect.right > WIDTH:
            self.game.load_new_map("level2.txt")
            self.rect.left = 0

        elif self.rect.top < 0:
            self.game.load_new_map("level2.txt")
            self.rect.bottom = HEIGHT

        elif self.rect.bottom > HEIGHT:
            self.game.load_new_map("level2.txt")
            self.rect.top = 0


# Function to load and render a tilemap
def load_tilemap(tilemap):
    screen.fill((0, 0, 0))  # Fill screen with black (background)
    for row in range(len(tilemap)):
        for col in range(len(tilemap[row])):
            tile = tilemap[row][col]
            if tile == 1:
                pg.draw.rect(screen, (255, 255, 255), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


        # # print(self.cd.ready())
        # if not self.cd.ready():
        #     self.image = self.game.player_img_inv
        #     # self.rect = self.image_inv.get_rect()
        #     print("not ready")
        # else:
        #     # self.image.fill(GREEN)
        #     self.image = self.game.player_img
        #     # self.rect = self.image.get_rect()
        #     print("ready")


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        self.image = self.game.mob_img
        Sprite.__init__(self, self.groups)
       # self.image = pg.Surface((32, 32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.vel = vec(choice([-1,1]),choice([-1,1]))
        self.pos = vec(x,y)*TILESIZE[0]
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        self.speed = 5
        print(self.pos)
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # print(self.pos)
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                self.vel.x *= choice([-1,1])
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.rect.y = self.pos.y
                self.vel.y *= choice([-1,1])
    def update(self):
        # mob behavior
        if self.game.player.pos.x > self.pos.x:
            self.vel.x = 1
        else:
            self.vel.x = -1
            # print("I don't need to chase the player x")
        if self.game.player.pos.y > self.pos.y:
            self.vel.y = 1
        else:
            self.vel.y = -1
            # print("I don't need to chase the player x")
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y *TILESIZE[1]
        # coin behavior
        pass
class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0] 
        self.state = state
        # print("wall created at", str(self.rect.x), str(self.rect.y))
    
                    
    def collide_with_walls(self, dir):
         if dir == 'x':
             hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
             if hits:
                
                 # print(self.pos)
                 if self.vel.x > 0:
                     print("a wall collided with a wall")
                     if hits[0].state == "moveable":
                         print("i hit a moveable block...")
                         hits[0].pos.x += self.vel.x
                         if len(hits) > 1:
                             if hits[1].state == "unmoveable":
                                 self.pos.x = hits[1].rect.left - self.rect.width
                     else:
                         self.pos.x = hits[0].rect.left - self.rect.width
                        
                 if self.vel.x < 0:
                     if hits[0].state == "moveable":
                         print("i hit a moveable block...")
                         hits[0].pos.x += self.vel.x
                         if len(hits) > 1:
                             if hits[1].state == "unmoveable":
                                 self.pos.x = hits[1].rect.right
                     else:
                         self.pos.x = hits[0].rect.right
                 self.vel.x = 0
                 self.rect.x = self.pos.x
         if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                 # print(self.pos)
                
                 if self.vel.y > 0:
                     print('wall y collide down')
                     if hits[0].state == "moveable":
                         print("i hit a moveable block...")
                         hits[0].pos.y += self.vel.y
                         if len(hits) > 1:
                             if hits[1].state == "unmoveable":
                                 self.pos.y = hits[1].rect.top - self.rect.height
                     else:
                         self.pos.y = hits[0].rect.top - self.rect.height
                        
                 if self.vel.y < 0:
                     if hits[0].state == "moveable":
                         print("i hit a moveable block...")
                         hits[0].pos.y += self.vel.y
                         if len(hits) > 1:
                             if hits[1].state == "unmovable":
                                 self.pos.y = hits[1].rect.bottom
                     else:
                         self.pos.y = hits[0].rect.bottom
                 self.vel.y = 0
                 self.rect.y = self.pos.y
 
    def update(self):
        # wall
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Projectile(Sprite):
    def __init__(self, game, x, y, dir):
        self.game = game
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = dir
        self.pos = vec(x,y)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print
    def update(self):
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits:
            self.kill()
class Attack(pg.sprite.Sprite):
    def __init__(self, game, x, y, dir):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        # small rectangle to represent the melee attack
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.topleft = self.pos

        # attack direction
        if dir.length() == 0:
            self.vel = vec(1, 0)  # default right
        else:
            self.vel = dir * 10

        self.lifetime = 200  # milliseconds
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        # move attack
        self.pos += self.vel
        self.rect.topleft = self.pos

        # remove attack after lifetime
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

        # check collision with mobs
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if hits:
            self.kill()
