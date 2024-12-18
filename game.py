import pygame
from pygame.locals import QUIT
import random
from game_object import GameObject
from ball import Ball

class Game:
    GAME_SPEED = 1
    PLAYER_SPEED = 0.5 * GAME_SPEED
    DEFENDER_SPEED = 0.25 * GAME_SPEED
    CONE_SPEED = 0 * GAME_SPEED
    BALL_SPEED = 0.7 * GAME_SPEED
    POWER_SHOT = 0.5 * GAME_SPEED
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 440
    MID_X = SCREEN_WIDTH // 2
    MID_Y = SCREEN_HEIGHT // 2
    SCREEN_BORDER = 25
    CONE_WIDTH, CONE_HEIGHT = 20, 20
    PLAYER_WIDTH, PLAYER_HEIGHT = 35, 60
    DEFENDER_WIDTH, DEFENDER_HEIGHT = 45, 60
    BALL_SIZE = 20
    GOAL_WIDTH = 125
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    
    def __init__(self):
        # initilaise pygame
        pygame.init()
        pygame.font.init()
        
        #set screen size and title 
        pygame.display.set_caption('Soccer')
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))  
        
        # set background image
        self.background_image = pygame.image.load('images/half_soccer_pitch.jpg')
        self.background_image = pygame.transform.scale(self.background_image, \
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))    
        self.player = GameObject(x=self.MID_X, y=self.SCREEN_HEIGHT-self.PLAYER_HEIGHT, \
            speed=self.PLAYER_SPEED)
        self.player.set_image('images/player.png', self.PLAYER_WIDTH, self.PLAYER_HEIGHT)
        self.defender1 = GameObject(x=self.MID_X, y=self.MID_Y-self.DEFENDER_HEIGHT, \
            speed=self.DEFENDER_SPEED, limit_border=125)
        self.defender1.set_image('images/defender.png', self.DEFENDER_WIDTH, self.DEFENDER_HEIGHT)
        self.defender2 = GameObject(x=self.MID_X, y=self.MID_Y-self.DEFENDER_HEIGHT*2, \
            speed=self.DEFENDER_SPEED, limit_border=125)
        self.defender2.set_image('images/defender.png', self.DEFENDER_WIDTH, self.DEFENDER_HEIGHT)
        self.cone1 = GameObject(x=self.MID_X-self.GOAL_WIDTH//2-self.CONE_WIDTH, y=0, \
            speed=self.CONE_SPEED)
        self.cone1.set_image('images/cone.png', self.CONE_WIDTH, self.CONE_WIDTH)
        self.cone2 = GameObject(x=self.MID_X+self.GOAL_WIDTH//2, y=0, speed=self.CONE_SPEED)
        self.cone2.set_image('images/cone.png', self.CONE_WIDTH, self.CONE_HEIGHT)
        self.ball = Ball(speed=self.BALL_SPEED, power=0, curve_amount=0.5)
        self.ball.set_image('images/soccer_ball.png', self.BALL_SIZE, self.BALL_SIZE)
        self.ball.hide = True
        
        self.objects = [self.player, self.defender1, self.defender2, self.ball, self.cone1, self.cone2] 
        
    def render_text(self, text, font_size=72, color=BLACK, x=0, y=0, x_offset=0, \
        y_offset=0, center=True):
        font = pygame.font.SysFont('Aptos', font_size)
        render = font.render(text, True, color)
        if center: 
            text_rect = render.get_rect(center=(self.MID_X + x_offset, \
            self.MID_Y + y_offset))
            self.screen.blit(render, text_rect)
        else:
            self.screen.blit(render, (x, y))
        
    def end_screen(self, goals, misses):
        self.screen.blit(self.background_image, (0, 0))
        self.render_text(f'Goals: {goals} Misses: {misses}', font_size=35, y_offset=-50)
        self.render_text(f'Accuracy: {int((goals/10)*100)}%')
        self.render_text(text=f'Play again? y/n', font_size=50, y_offset=60)
        pygame.display.update()
         
        end_screen = True
        while end_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_screen = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        end_screen = False
                        break
                    if event.key == pygame.K_y:
                        self.run_game()
                        end_screen = False
                        break
                
    def player_on_screen(self):
        return self.MID_Y > self.player.y > self.player.y_startpos and \
            0 < self.player.x < self.SCREEN_WIDTH-self.PLAYER_WIDTH

    def ball_on_screen(self):
        ball_onscreen = -self.BALL_SIZE <= self.ball.x <= self.SCREEN_WIDTH-self.BALL_SIZE and \
            -self.BALL_SIZE <= self.ball.y <= self.SCREEN_HEIGHT
        return ball_onscreen

    def hide_ball(self):
        self.ball.y, self.ball.x = -20, -20

    def ball_hit_defender(self, defender):
        return (defender.x <= self.ball.x <= defender.x+self.DEFENDER_WIDTH) and \
            (defender.y <= self.ball.y <= defender.y+self.DEFENDER_HEIGHT)

    def ball_hit_cone(self, cone):
        return 0 <= self.ball.y <= self.CONE_HEIGHT and \
            (cone.x-self.CONE_WIDTH <= self.ball.x <= cone.x+self.CONE_WIDTH)

    def goal(self):
        return self.ball.y <= self.CONE_HEIGHT and \
            (self.cone1.x+self.BALL_SIZE/2 < self.ball.x < self.cone2.x-self.BALL_SIZE/2)

    def curve_ball(self, direction):
        self.ball.direction = direction
        self.ball.move()
        self.ball.direction = 'UP'
    
    def reset_ball(self):
        self.ball.direction = 'UP'
        self.ball.hide = True
        self.ball.power = 0
        self.ball.curve_left = False
        self.ball.curve_right = False
    
    def run_game(self):
        game_time, start_delay, goals, misses = 0, 0, 0, 0
        game_running = True
        goal_text = ''
        ball_kicked, goal = False, False
        
        # get key events
        while game_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.player.direction = 'RIGHT'    
                    if event.key == pygame.K_LEFT:
                        self.player.direction = 'LEFT'    
                        
                    #allow ball kick if not already kicked
                    if event.key == pygame.K_SPACE and not ball_kicked:
                        #shoot the ball
                        ball_kicked = True
                        self.ball.hide = False
                        self.ball.x = self.player.x
                        self.ball.y = self.player.y
                        
                        #Get all pressed keys
                        keys = pygame.key.get_pressed()
                        # Check for specific key combinations
                        if keys[pygame.K_SPACE] and keys[pygame.K_UP]:
                            self.ball.power = self.POWER_SHOT
                        if keys[pygame.K_SPACE] and keys[pygame.K_LEFT]:
                            self.ball.curve_left = True
                            self.ball.kick_x = self.player.x - 70
                        if keys[pygame.K_SPACE] and keys[pygame.K_RIGHT]:
                            self.ball.curve_right = True
                            self.ball.kick_x = self.player.x - 110 - self.PLAYER_WIDTH//2              
            
            # increment game object movement
            for instance in [self.player, self.defender1, self.defender2, self.cone1, self.cone2]:
                if instance.x < 0 + instance.limit_border:
                    instance.direction = 'RIGHT'
                if instance.x > self.SCREEN_WIDTH - instance.limit_border:
                    instance.direction = 'LEFT'
                instance.move()
            
            # randomly change defender direction
            if random.randint(0, 10000) < 20:
                self.defender1.direction = random.choice(('LEFT', 'RIGHT'))
            if random.randint(0, 10000) < 30:    
                self.defender2.direction = random.choice(('LEFT', 'RIGHT'))
            
            # increment ball movement while kicked and still on screen 
            if ball_kicked:
                if self.ball_on_screen():
                    self.ball.move()
                    if self.goal():
                        goals += 1
                        goal = True
                        start_delay = game_time
                        ball_kicked = False
                        self.reset_ball()
                    elif self.ball_hit_defender(self.defender1) or self.ball_hit_defender(self.defender2):
                        self.hide_ball()
                    elif self.ball_hit_cone(self.cone1):
                        self.hide_ball()
                        self.cone1.y += -self.CONE_HEIGHT
                        start_delay = game_time
                    elif self.ball_hit_cone(self.cone2):
                        self.hide_ball()
                        self.cone2.y += -self.CONE_HEIGHT
                        start_delay = game_time
                        
                else:
                    misses += 1
                    ball_kicked = False
                    self.reset_ball()
            
            # show goal text if it's a goal
            if goal:
                goal_text = 'GOAL!!'
                
            # delay resetting cones and clearing goal text
            if game_time == start_delay + 200:
                self.cone1.y, self.cone2.y = 0, 0
                goal_text = ''
                goal = False
            
            # render game components on screen        
            self.screen.blit(self.background_image, (0, 0))
            self.render_text(text=f'Goals: {goals}', font_size=25, x=0, y=0, center=False)
            self.render_text(text=f'Misses: {misses}', font_size= 25, x=self.SCREEN_WIDTH-80, y=0, \
                center=False)
            self.render_text(text=goal_text, color=self.RED)
            if self.ball.power != 0:
                self.render_text(text='P', font_size=25, x=0, y=self.SCREEN_HEIGHT-20, center=False)
            
            for instance in self.objects:
                instance.show(self.screen)
            
            # Update the display
            pygame.display.update()
            
            # increment time
            game_time += 1
            
            if goals+misses >= 10:
                break
        
        self.end_screen(goals, misses)

Game().run_game()


