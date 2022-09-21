import pygame
import random
import sys
import math
from pygame.locals import *
from settings import *
from sprites import *
from pygame import mixer 



class Game:
    def __init__(self):        
        pygame.init()
        pygame.mixer.init()
        self.win = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.bg = pygame.image.load(CITY_BG)
        self.bg = pygame.transform.scale(self.bg, (GAME_WIDTH, GAME_HEIGHT))
        self.font = pygame.font.SysFont('Arial',30,True,)  #style,size,bold=T,Italic=F
        self.fontGO = pygame.font.SysFont('Arial',60,True,)
        
        # Load Sounds
        self.bg_music = pygame.mixer.Sound(BG_MUSIC)
        self.bullet_snd = pygame.mixer.Sound(BULLET_SOUND) 
        
        # Sprite Groups
        self.ufos = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.ufo_projectiles = pygame.sprite.Group()
        self.ufo1_projectiles = pygame.sprite.Group()
        self.ufo2_projectiles = pygame.sprite.Group()
        self.plasmas = pygame.sprite.Group()    # Projectile: Plasma
        self.rockets = pygame.sprite.Group()    # Player Projectile: Rocket
        self.obstacles = pygame.sprite.Group()
        
        # Tutorial
        self.start_font = pygame.font.SysFont('Cooper Black', 40)
        self.start_title = self.start_font.render('Press SPACE to start the game!', True, RED)
        self.move_font = pygame.font.SysFont('Cooper Black', 20)
        self.forward_arrow = self.move_font.render('Move Forward', True, RED)
        self.back_arrow = self.move_font.render('Move Back', True, RED)
        self.jump_arrow = self.move_font.render('Jump', True, RED)
        self.shoot_arrow = self.move_font.render('Shoot', True, RED)
        self.logo = pygame.image.load(GAME_LOGO)
        self.forward_pic = pygame.image.load(RIGHT_ARROW)
        self.back_pic = pygame.image.load(LEFT_ARROW)
        self.shoot_pic = pygame.image.load(SPACE_BAR)
        self.jump_pic = pygame.image.load(UP_ARROW)
        self.logo = pygame.transform.scale(self.logo, (900, 782))
        self.forward_pic = pygame.transform.scale(self.forward_pic, (55,25))
        self.back_pic = pygame.transform.scale(self.back_pic, (55,25))
        self.shoot_pic = pygame.transform.scale(self.shoot_pic, (55,35))
        self.jump_pic = pygame.transform.scale(self.jump_pic, (25,30))
        self.tutorial = True
        
        pygame.time.set_timer(EVENT_OBSTACLE, random.randrange(3000,6500))
        self.done = False
        
        self.bg_music.play(-1)
        self.new_game()
    
    def new_game(self):
        self.score = 0
        self.final_score = 0
        self.scroll_X = 0 #metablhth pou xrhsimopoioume gia na kinoume to background
        self.ufos.empty()
        self.player_projectiles.empty()
        self.ufo_projectiles.empty()
        self.ufo1_projectiles.empty()
        self.ufo2_projectiles.empty()
        self.plasmas.empty()
        self.rockets.empty()
        self.obstacles.empty()
        self.car = Player(self)
        self.ufo1 = UFO(self, 'UFO-1', 230, 15, 3, 20, 600, hitbox_height=30)
        self.ufo2 = UFO(self, 'UFO-2', 240, 95, 5, 20, 700)  
        self.total_seconds = 0
        self.frame_count = 0
        self.clock = pygame.time.Clock()
        self.game_over = False


    def draw(self):
        if not self.game_over and not self.tutorial:
            # Blit bg
            self.win.blit(self.bg, (self.rel_x - self.bg.get_rect().width, 0))
            # Draw text
            timer_text = self.font.render('Timer : ' + str(self.total_seconds), 1, RED)
            score_text = self.font.render('Score: ' + str(self.score), 1, BLUE)
            health_text = self.font.render('Lives: ' + str(self.car.health), 1, GREEN)
            self.win.blit(timer_text, (850,10))
            self.win.blit(score_text, (850,35))
            self.win.blit(health_text, (850,60))
            # Draw sprites
            self.car.draw(self.win)
            for ufo in self.ufos:
                ufo.draw(self.win)
            for obstacle in self.obstacles:
                obstacle.draw(self.win)
            for player_projectile in self.player_projectiles:
                player_projectile.draw(self.win)
            for ufo_projectile in self.ufo_projectiles:
                ufo_projectile.draw(self.win)
        elif self.game_over:
            # Fill Black
            self.win.fill(BLACK)
            # Draw text
            death_text = self.fontGO.render('GAME OVER', 1, RED)
            time_played_text = self.font.render('Time played : ' + str(self.total_seconds), 1, RED)
            score_text = self.font.render('Score: ' + str(self.score), 1, RED)
            final_score_text = self.font.render('Final Score: ' + str(self.final_score), 1, RED)
            keys_text = self.font.render('Hit Esc to Quit or Enter to Restart', 1, RED)
            self.win.blit(death_text, (300,80))
            self.win.blit(time_played_text, (300,190))
            self.win.blit(score_text, (300,270))
            self.win.blit(final_score_text, (300,310))
            self.win.blit(keys_text, (300,400))
        elif self.tutorial:
            self.win.fill(BLACK)
            self.win.blit(self.start_title,(160,410))
        
            
            
            self.win.blit(self.logo, (60,-300))
            self.win.blit(self.forward_pic, (400,200))
            self.win.blit(self.forward_arrow, (470,200))       
            self.win.blit(self.back_pic, (400,250))
            self.win.blit(self.back_arrow, (470,250))
            self.win.blit(self.shoot_pic, (400,300))
            self.win.blit(self.shoot_arrow, (470,300))      
            self.win.blit(self.jump_pic, (410,350))
            self.win.blit(self.jump_arrow, (470,350))
            
        pygame.display.flip()

    
    def update(self):
        if not self.game_over:
            # Background Scroll
            self.rel_x = self.scroll_X % self.bg.get_rect().width #metakinhsh eikonas     
            self.scroll_X -= SCROLL_SPEED

            if self.rel_x < GAME_WIDTH :
                self.win.blit(self.bg, (self.rel_x, 0))

            # Sprite Updates
            self.car.update()
            for ufo in self.ufos:
                ufo.update()
            for obstacle in self.obstacles:
                obstacle.update()
            for player_projectile in self.player_projectiles:
                player_projectile.update()
            for ufo_projectile in self.ufo_projectiles:
                ufo_projectile.update()
            
            self.total_seconds = self.frame_count // FPS
            self.frame_count += 1
                    
                
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            
            if not self.game_over:
                # Create random block + spikes
                if event.type == EVENT_OBSTACLE:
                    r = random.randrange(0,2)
                    if r == 0:                
                        self.obstacles.add(Obstacle(self, 'OBSTACLE_BLOCK', GAME_WIDTH + 30, 330))
                    else:
                        self.obstacles.add(Obstacle(self, 'OBSTACLE_SPIKES', GAME_WIDTH + 30, 250))
                # Ressurect aliens!
                if event.type == EVENT_UFO_1:
                    self.ufo1 = UFO(self, 'UFO-1', 230, 15, 3, 20, 600, hitbox_height=30)
                    pygame.time.set_timer(EVENT_UFO_1, 0)
                if event.type == EVENT_UFO_2:
                    self.ufo2 = UFO(self, 'UFO-2', 240, 95, 5, 20, 700)
                    pygame.time.set_timer(EVENT_UFO_2, 0)
                    


    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.tutorial:
            if keys[pygame.K_SPACE]:
                self.tutorial = False

        elif self.game_over:
            if keys[pygame.K_ESCAPE]:
                self.done = True
            if keys[pygame.K_RETURN]:
                self.new_game()
        
        else:
            # Shoot Plasma & Rockets
            if keys[pygame.K_SPACE] and self.car.shoot_cd == 0:
                self.bullet_snd.play()
                if len(self.plasmas) < 5:
                    Projectile(self, 'PLAYER_PLASMA', round(self.car.rect.x + 20 + self.car.rect.width // 2), round(self.car.rect.y + 15 + self.car.rect.height // 2))
                    self.car.shoot_cd += 1
                if len(self.rockets) < 5:
                    Projectile(self, 'PLAYER_ROCKET', round(self.car.rect.x + 30 + self.car.rect.width // 2), round(self.car.rect.y + 15 + self.car.rect.height // 2))
                    self.car.shoot_cd += 1

            # Movement
            if keys[pygame.K_LEFT] and self.car.rect.x > self.car.vel.x:
                self.car.rect.x -= self.car.vel.x           
            if keys[pygame.K_RIGHT] and self.car.rect.x < GAME_WIDTH - self.car.rect.width - self.car.vel.x:
                self.car.rect.x += self.car.vel.x

            # Jumping
            if not self.car.isJump:
                if keys[pygame.K_UP]:
                    self.car.isJump = True
        


    def loop(self):
        while not self.done:
            if self.car.health == 0:
                self.game_over = True
            self.event()
            self.input()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()



game = Game()
game.loop()