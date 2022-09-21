import pygame
import random
import sys
import math
from pygame.locals import *
from settings import *
from pygame import mixer




class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.rect = pygame.Rect((PLAYER_START_POS_X, PLAYER_START_POS_Y), (CAR_WIDTH, CAR_HEIGHT))
        self.image = pygame.image.load(CAR_SPRITE)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.vel = pygame.math.Vector2(PLAYER_VEL_X, PLAYER_VEL_Y)
        self.isJump = False
        self.walkCount = 0
        self.m = 1                                                          #m is for jump function
        self.hitbox = self.rect
        self.health = PLAYER_HEALTH
        self.shoot_cd = 0
        

    def update(self):
        # Refresh cooldowns
        if self.shoot_cd > 0:
            self.shoot_cd += 1
        if self.shoot_cd > 20:                                              #change player bullet cooldown
            self.shoot_cd = 0

        # Jump
        if self.isJump:
            #increasing v increases altitude
            F = (1/4) * self.m * (self.vel.y ** 2)
            self.rect.y -= F 
            self.vel.y = self.vel.y - 0.5
            
            #megisto upsos 
            if self.vel.y < 0:  
                self.m =-1
                    
            #This vel.y must -11 more than original vel.y 
            if self.rect.y >= PLAYER_START_POS_Y:
                self.rect.y = PLAYER_START_POS_Y
                self.isJump = False
                self.vel.y = 9
                self.m = 1

    def draw(self, win):
        win.blit(self.image, self.rect)
        if DEBUG_HITBOXES:
            pygame.draw.rect(win,(255,0,0), self.hitbox, 2)
        
    def hit(self):
        self.rect.x = PLAYER_START_POS_X
        self.rect.y = PLAYER_START_POS_Y
        self.vel.y = 9
        self.m = 1
        self.isJump = False
        # Reset game values
        self.game.ufo_projectiles.empty()
        self.game.ufo1_projectiles.empty()
        self.game.ufo2_projectiles.empty()
        self.game.player_projectiles.empty()
        self.game.plasmas.empty()
        self.game.rockets.empty()
        self.game.ufo_projectiles.empty()
        self.game.obstacles.empty()
        print('lost a life')
        

    
class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, kind, x, y):
        if kind == 'PLAYER_PLASMA':
            super().__init__(game.player_projectiles, game.plasmas)
            self.color = RED
            self.vel = 9                                                     #change plasma speed
        elif kind == 'PLAYER_ROCKET':
            super().__init__(game.player_projectiles, game.rockets)
            self.color = PURPLE
            self.vel = -9                                                    #change rocket speed
        elif kind == 'UFO1_BEAM':
            super().__init__(game.ufo_projectiles)
            self.color = GREEN
            self.vel = 3                                                     #change UFO1 bullet speed
        elif kind == 'UFO2_BEAM':
            super().__init__(game.ufo_projectiles)
            self.color = GREEN2
            self.vel = 2                                                     #change UFO2 bullet speed
        else:
            print('ERROR: Lathos typos Projectile.')
        self.game = game
        self.kind = kind
        self.x = x
        self.y = y
        self.radius = 6

    def draw(self, win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

    def update(self):
        # Collisions
        if self.kind in ['UFO1_BEAM', 'UFO2_BEAM']:
            if (self.y - self.radius < self.game.car.hitbox[1] + self.game.car.hitbox[3] and self.y + self.radius > self.game.car.hitbox[1]) and (self.x - self.radius > self.game.car.hitbox[0] and self.x - self.radius < self.game.car.hitbox[0] + self.game.car.hitbox[2]):
                self.game.car.hit()
                self.game.car.health -= 1
                print('car got shot down')
                self.kill()
        if self.kind == 'PLAYER_ROCKET':
            for ufo in self.game.ufos:
                if (self.y - self.radius < ufo.hitbox[1] + ufo.hitbox[3] and self.y + self.radius > ufo.hitbox[1]) and (self.x - self.radius > ufo.hitbox[0] and self.x - self.radius < ufo.hitbox[0]+ ufo.hitbox[2]):
                    ufo.hit()
                    self.game.score += 1
                    self.game.final_score = self.game.total_seconds + self.game.score * 100
                    self.kill()
        if self.kind == 'PLAYER_PLASMA':
            for obstacle in self.game.obstacles:
                    if obstacle.hit( pygame.Rect((self.x - self.radius*2, self.y - self.radius*2), (self.radius*2, self.radius*2)) ):
                        if obstacle.kind == 'OBSTACLE_BLOCK':
                            self.game.score += 1
                            self.game.final_score = self.game.total_seconds + self.game.score * 100
                            obstacle.kill()
                        self.kill()

        # Movement
        if (self.x > 0 and self.x < GAME_WIDTH) and (self.y > 0 and self.y < GAME_HEIGHT):
            if self.kind in ['PLAYER_ROCKET', 'UFO1_BEAM', 'UFO2_BEAM']:
                self.y += self.vel                                           #+ - makes projectile go up or down
            else:
                self.x += self.vel
        else:
            self.kill()
          


class UFO(pygame.sprite.Sprite):        
    def __init__(self, game, model, x, y, vel, start, end, hitbox_height=False):
        super().__init__(game.ufos)
        self.game = game
        self.model = model if model in ['UFO-1', 'UFO-2'] else 'UFO-1'
        self.rect = pygame.Rect((x, y), (UFO1_WIDTH, UFO1_HEIGHT) if self.model == 'UFO-1' else (UFO2_WIDTH, UFO2_HEIGHT))
        self.image = pygame.image.load(UFO1_SPRITE if self.model == 'UFO-1' else UFO2_SPRITE)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.set_alpha(255)
        self.hitbox = self.rect
        if hitbox_height:
            self.hitbox.height = hitbox_height
        self.vel = vel
        self.path = [start, end]
        self.shoot_cd = 0
                
    def draw (self, win):
        self.move()
        win.blit(self.image, self.rect)
        if DEBUG_HITBOXES:
            pygame.draw.rect(win, RED, self.rect, 2)
        
    def move(self):
        if self.vel > 0:
            if self.rect.x + self.vel < self.path[1]:
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.rect.x - self.vel > self.path[0]:
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
         
    def hit(self):
        print('ufo hit')
        self.kill()
        # Ressurect in 10/15 secs
        if self.model == 'UFO-1':
            pygame.time.set_timer(EVENT_UFO_1, 10000)   # 10s
        elif self.model == 'UFO-2':
            pygame.time.set_timer(EVENT_UFO_2, 15000)   # 15s

    def update(self):
        # Refresh cooldowns
        if self.shoot_cd > 0:
            self.shoot_cd += 1
        if self.shoot_cd > 25:                                              #change UFO bullet cooldown
            self.shoot_cd = 0

        # Create Projectiles
        if self.shoot_cd == 0:
            if self.model == 'UFO-1' and len(self.game.ufo1_projectiles) < 1:
                self.game.ufo1_projectiles.add(Projectile(self.game, 'UFO1_BEAM', round(self.rect.x + 10 + self.rect.width // 2), round(self.rect.y + 25 + self.rect.height //2)))
                self.shoot_cd += 1
            elif self.model == 'UFO-2' and len(self.game.ufo2_projectiles) < 3:
                self.game.ufo2_projectiles.add(Projectile(self.game, 'UFO2_BEAM', round(self.rect.x + 10 + self.rect.width // 2), round(self.rect.y + 20 + self.rect.height //2)))
                self.shoot_cd += 1



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, kind, x, y):
        super().__init__(game.obstacles)
        if kind == 'OBSTACLE_BLOCK':
            self.rect = pygame.Rect((x, y), (BLOCK_WIDTH, BLOCK_HEIGHT))
            self.image = pygame.image.load(BLOCK_SPRITE)
        elif kind == 'OBSTACLE_SPIKES':
            self.rect = pygame.Rect((x, y), (SPIKES_WIDTH, SPIKES_HEIGHT))
            self.image = pygame.image.load(SPIKES_SPRITE)
        else:
            print('ERROR: Lathos typos Obstacle.')
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.set_alpha(255)
        self.hitbox = self.rect
        if kind == 'OBSTACLE_SPIKES':
            self.hitbox = pygame.Rect((x, y + y/3), (BLOCK_WIDTH, BLOCK_HEIGHT - BLOCK_HEIGHT / 3))
        else:
            self.hitbox = pygame.Rect((x, y), (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.game = game
        self.kind = kind
        super().__init__(game.obstacles)

    def update(self):
        self.rect.x -= SCROLL_SPEED
        self.hitbox.x -= SCROLL_SPEED
            
        if self.hit(self.game.car.hitbox):
            print('car got hit lives -1')
            self.game.car.hit()
            self.game.car.health -= 1            
            self.kill()

        if self.rect.x < self.rect.width * -1:
            self.kill()

    def draw(self, win):
        win.blit(self.image, [self.rect.x, self.rect.y])
        if DEBUG_HITBOXES:
            pygame.draw.rect(win, RED, self.hitbox, 2)
    
    def hit(self, rect):
        if (rect[0] + rect[2] > self.hitbox[0] and rect[0]  < self.hitbox[0] + self.hitbox[2]) and (rect[1] + rect[3] >self.hitbox[1]):
            if self.kind == 'OBSTACLE_BLOCK':
                self.kill()
            return True
        return False
