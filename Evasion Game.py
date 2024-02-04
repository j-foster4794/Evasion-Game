import pygame
import random
import time
import math
from pygame.locals import *

screen_width = 1000
screen_height = 1000

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

class Player(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    image = pygame.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Evasion Game\EvasionGamePlayer.png").convert()                 #Add new file
    image = pygame.transform.scale(image, (50, 50))
    self.surf = image
    self.rect = self.surf.get_rect(center=(screen_width / 2,screen_height / 2))

  def update(self, pressed_keys):
    if pressed_keys[pygame.K_UP]:
      self.rect.move_ip(0, -1)
    if pressed_keys[pygame.K_DOWN]:
      self.rect.move_ip(0, 1)
    if pressed_keys[pygame.K_LEFT]:
      self.rect.move_ip(-1, 0)
    if pressed_keys[pygame.K_RIGHT]:
      self.rect.move_ip(1, 0)


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
player = Player()


class enemy(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    image = pygame.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Evasion Game\EvasionGameEnemy.png").convert()                     #Add new file
    image = pygame.transform.scale(image, (50, 50))
    self.surf = image
    area = random.choice(["t", "b", "r", "l"])
    if area == "t":
      spawnwidth = random.randint(-25, screen_width + 25)
      spawnheight = random.randint(-25, 0)
    elif area == "b":
      spawnwidth = random.randint(-25, screen_width + 25)
      spawnheight = random.randint(screen_height, screen_height + 25)
    elif area == "l":
      spawnwidth = random.randint(-25, 0)
      spawnheight = random.randint(-25, screen_height + 25)
    elif area == "r":
      spawnwidth = random.randint(screen_width, screen_width + 25)
      spawnheight = random.randint(-25, screen_height + 25)
    self.rect = self.surf.get_rect(center=(spawnwidth, spawnheight))
    direction = (spawnwidth - player.rect.center[0],
                 spawnheight - player.rect.center[1])
    distance = math.sqrt(direction[0]**2 + direction[1]**2)
    self.xmove, self.ymove = (direction[0] // 1), (direction[1] // 1)
  def move(self):
    global player
    self.position = [self.rect.x, self.rect.y]
    direction = (self.position[0] - player.rect.center[0],
                 self.position[1] - player.rect.center[1])
    distance = math.sqrt(direction[0]**2 + direction[1]**2)
    if distance != 0:
      direction = (direction[0] / distance, direction[1] / distance)
    speed = random.randint(1,3)
    self.rect.x -= int(direction[0] * speed)
    self.rect.y -= int(direction[1] * speed)
   

    if self.rect.right < -50 or self.rect.left > screen_width + 50 or self.rect.bottom > screen_height + 50 or self.rect.top < -50:
      self.kill()


def outputvisuals():
  screen.fill((0,0,0))
  for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)
  pygame.display.flip()


def entitiesupdate():
  global pressed_keys
  pressed_keys = pygame.key.get_pressed()
  player.update(pressed_keys)
  for bad in enemies:
    if timer % 10 == 0:
      bad.move()


def eventhandling():
  global running 
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[pygame.K_ESCAPE]:
    running = False
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == ADDENEMY:
      new_enemy = enemy()
      enemies.add(new_enemy)
      all_sprites.add(new_enemy)


enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
running = True
timer = 0

deathscreen = pygame.image.load("H:\James School Work\A Level\Comp Sci\Coding\Python Coding\Evasion Game\EvasionGameDeathScreen.png").convert()   # Add new file
deathscreen = pygame.transform.scale(deathscreen,(screen_width, screen_height))

alive = True

while running:

  if alive == True:
    entitiesupdate()
    outputvisuals()
    eventhandling()
  else:
    eventhandling()
    screen.blit(deathscreen, (0, 0))
    pygame.display.flip()
  if pygame.sprite.spritecollideany(player, enemies):
    player.kill()
    alive = False
  timer += 1

pygame.quit()