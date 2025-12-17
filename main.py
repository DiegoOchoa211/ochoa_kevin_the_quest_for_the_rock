# Created by Diego Ochoa with the help of ChatGPT
#Design Goals/Rules
#4 Levels so far
#The Rock Boss at the end
#transitions for all rooms
# goal of game is get to final level and beat the boss
# no start/pause/end screen yet
# import necessary modules
# core game loop
# input
# update
# draw

import math
import random 
import sys
import pygame as pg
from settings import *
from sprites import *
from os import path
from utils import *
from math import floor

# overview - CONCISE AND INFORMATIVE
class Game:
   def __init__(self):
      pg.init()
      pg.mixer.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Kevin: The Quest for the Rock")
      self.playing = True
      self.enemies_defeated = 0 
      self.levels = ["level1.txt", "level2.txt", "level3.txt", "level4.txt", "level5.txt"]
      self.current_level_index = 0

   
   # sets up a game folder directory path using the current folder containing THIS file
   # give the Game class a map property which uses the Map class to parse the level1.txt file
   # loads image files from images folder
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.img_folder = path.join(self.game_folder, 'img')
      self.snd_folder = path.join(self.game_folder, 'sound')
                        #self.jump_sounds = pg.mixer.Sound(path.join(self.snd_folder, 'Jump33.wav'))
      #self.map = Map(path.join(self.game_folder, 'level1.txt'))
      self.map = Map(path.join(self.game_folder, self.levels[self.current_level_index]))
      # loads image into memory when a new game is created and load_data is called
      self.player_img = pg.image.load(path.join(self.img_folder, 'kevin.png')).convert_alpha()
      self.mob_img = pg.image.load(path.join(self.img_folder, 'rock_pixel_small.png')).convert_alpha()
      self.player_img_inv = pg.image.load(path.join(self.img_folder, 'kevin.png')).convert_alpha()
      self.mob_img_inv = pg.image.load(path.join(self.img_folder, 'rock_pixel_small.png')).convert_alpha()
      self.bg_img = pg.image.load(path.join(self.img_folder, 'backround.png')).convert_alpha()
      self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
   
      #self.bg_img = pg.image.load(path.join(self.img_folder, 'terrain.png')).convert_alpha()
      #self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
   def new(self):
      # the sprite Group allows us to upate anwd draw sprite in grouped batches
      self.load_data()
      # create all sprite groups
      self.all_sprites = pg.sprite.Group()
      self.all_mobs = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
      self.all_projectiles = pg.sprite.Group()
      for row, tiles, in enumerate(self.map.data):
         # print(row)
         for col, tile, in enumerate(tiles):
            # print(col)
            if tile == '1':
               Wall(self, col, row, "unmoveable")
            if tile == '2':
               Wall(self, col, row, "moveable")
            elif tile == 'C':
               Coin(self, col, row)
            elif tile == 'P':
               self.player = Player(self, col, row)
            elif tile == 'M':
               Mob(self, col, row)


   def load_new_map(self, filename):
    player_coins = self.player.coins if self.player else 0
    player_health = self.player.health if self.player else 100

    # Clear old sprites
    self.all_sprites.empty()
    self.all_walls.empty()
    self.all_mobs.empty()
    self.all_coins.empty()
    self.all_projectiles.empty()
    self.player = None

    # Load the new map file
    self.map = Map(path.join(self.game_folder, filename))

    # Rebuild world from the new tilemap
    for row, tiles in enumerate(self.map.data):
        for col, tile in enumerate(tiles):
            if tile == '1':
                Wall(self, col, row, "unmoveable")
            elif tile == '2':
                Wall(self, col, row, "moveable")
            elif tile == 'C':
                Coin(self, col, row)
            elif tile == 'P':
               self.player = Player(self, col, row)
               self.player.coins = player_coins
               self.player.health = player_health
               self.player.pos = vec(col, row) * TILESIZE[0]
               self.player.rect.topleft = self.player.pos
            elif tile == 'M':
                Mob(self, col, row)
            elif tile == 'B':
               self.boss = Boss(self, col, row)
               self.boss_alive = True

            if self.player:
               if self.player.pos.x > WIDTH - TILESIZE[0]:
                  self.player.pos.x = TILESIZE[0]
                  self.player.rect.x = TILESIZE[0]
      
   def show_start_screen(self):
    waiting = True
    self.screen.fill(GREY)
    self.draw_text(self.screen, "Kevin: The Quest for the Rock", 60, BLACK, WIDTH//2, HEIGHT//3)
    self.draw_text(self.screen, "Created by Diego Ochoa", 32, BLACK, WIDTH//2, HEIGHT//3 + 80)
    self.draw_text(self.screen, "Click to Start", 40, BLACK, WIDTH//2, HEIGHT//2 + 100)
    pg.display.flip()

    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                waiting = False

   def show_win_screen(self):
    waiting = True
    self.screen.fill(GOLD)
    self.draw_text(self.screen, "TITAN SLAIN", 80, BLACK, WIDTH//2, HEIGHT//2 - 60)
    self.draw_text(self.screen, "Click to return to Start", 40, BLACK, WIDTH//2, HEIGHT//2 + 40)
    pg.display.flip()

    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                waiting = False


   def show_death_screen(self):
    waiting = True
    self.screen.fill(RED)
    self.draw_text(self.screen, "YOU DIED", 80, BLACK, WIDTH//2, HEIGHT//2 - 50)
    self.draw_text(self.screen, "Click to Retry", 40, BLACK, WIDTH//2, HEIGHT//2 + 50)
    pg.display.flip()

    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                waiting = False

   def reset_to_start(self):
    self.current_level_index = 0
    self.enemies_defeated = 0
    self.new()


   def run(self):
      while self.playing == True:
         self.dt = self.clock.tick(FPS) / 1000
         # input
         self.events()
         # process
         self.update()
         # output
         self.draw()
      pg.quit()

   def events(self):
      for event in pg.event.get():
        if event.type == pg.QUIT:
         #  print("this is happening")
          self.playing = False
        if event.type == pg.MOUSEBUTTONDOWN:
           print("I can get input from mouse")
   def update(self):
      self.all_sprites.update()
      seconds = pg.time.get_ticks()//1000
      countdown = 10
      self.time = countdown - seconds
      # if len(self.all_coins) == 0:
      #    for i in range(2,5):
      #       Coin(self, randint(1, 20), randint(1,20))
      #    print("I'm BROKE!")
      if self.player.pos.x > WIDTH - TILESIZE[0]:   #crossing right side of screen
         self.current_level_index += 1
         if self.current_level_index < len(self.levels):
            self.load_new_map(self.levels[self.current_level_index])
         else:
            self.playing = False  #no more levels


   def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
        #self.screen.blit(self.bg_img, (0,0))
   
   def draw_health_bar(self, x, y, width, height, health, max_health):
   # creates bar at bottom of screen for health/coins/mobs
    pg.draw.rect(self.screen, GREY, (x, y, width, height))
    ratio = max(0, health / max_health)
    health_width = int(width * ratio)
    # Red health bar
    pg.draw.rect(self.screen, RED, (x, y, health_width, height))

   
   
   def draw(self):
      self.screen.blit(self.bg_img, (0, 0))
      #self.screen.fill(WHITE)
      #self.draw_text(self.screen, str(self.time), 24, BLACK, 500, 100)
      self.all_sprites.draw(self.screen)

      #bottom UI bar
      bar_height = 40
      bar_y = HEIGHT - bar_height
      pg.draw.rect(self.screen, DARKGREY, (0, bar_y, WIDTH, bar_height))
      #draws health bar
      self.draw_health_bar(20, bar_y +5, 200, 30, self.player.health, 100)
      #coin counter
      self.draw_text(self.screen, f"Coins: {self.player.coins}",24,BLACK,260, bar_y + 10)
      #mob kill counter
      self.draw_text(self.screen, f"Mobs defeated: {self.enemies_defeated}",24,BLACK,450,bar_y + 10)

   # Boss health bar with help from AI
   #hasattr checks if two things exist
      if hasattr(self, "boss_alive") and self.boss_alive:
         bar_x = 150
         bar_y = 20
         bar_width = 500
         bar_height = 25
         pg.draw.rect(self.screen, DARKGREY, (bar_x, bar_y, bar_width, bar_height))
         boss_ratio = self.boss.health / self.boss.max_health
         pg.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width * boss_ratio, bar_height))
         self.draw_text(self.screen, "The Rock - Titan of Stone", 24, BLACK, bar_x + bar_width // 2, bar_y - 25)

      pg.display.flip()

   #def wait_for_key(self):
     # waiting = True
      #while waiting:
         #self.clock.tick(FPS)
         #for event in pg.event.get()
            #if event.type == pg.QUIT()
              # waiting = False
              # self.running = False
          #  if event.type
      


if __name__ == "__main__":
#    creating an instance or instantiating the Game class
   g = Game()
   g.show_start_screen()   
   g.new()
   g.run()
