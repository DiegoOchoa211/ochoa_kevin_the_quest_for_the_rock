# Created by Diego Ochoa with the help of ChatGPT
## import necessary modules
# core game loop
# input
# update
# draw

#yay i can use github from VS Code!
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
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Diego Ochoa's awesome game!!!!!")
      self.playing = True
   
   # sets up a game folder directory path using the current folder containing THIS file
   # give the Game class a map property which uses the Map class to parse the level1.txt file
   # loads image files from images folder
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.img_folder = path.join(self.game_folder, 'img')
      self.map = Map(path.join(self.game_folder, 'level1.txt'))
      # loads image into memory when a new game is created and load_data is called
      self.player_img = pg.image.load(path.join(self.img_folder, 'kevin.png')).convert_alpha()
      self.player_img_inv = pg.image.load(path.join(self.img_folder, 'kevin.png')).convert_alpha()
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
      if len(self.all_coins) == 0:
         for i in range(2,5):
            Coin(self, randint(1, 20), randint(1,20))
         print("I'm BROKE!")


   def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
        self.screen.blit(self.bg_img, (0,0))
   def draw(self):
      self.screen.fill(WHITE)
      self.draw_text(self.screen, str(self.player.health), 24, BLACK, 100, 100)
      self.draw_text(self.screen, str(self.player.coins), 24, BLACK, 400, 100)
      self.draw_text(self.screen, str(self.time), 24, BLACK, 500, 100)
      self.all_sprites.draw(self.screen)
      pg.display.flip()
      


if __name__ == "__main__":
#    creating an instance or instantiating the Game class
   g = Game()
   g.new()
   g.run()
