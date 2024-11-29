import pygame
import math

class GameObject:
        
    def __init__(self, x=0, y=0, speed=0, direction='RIGHT', image=None, \
        image_width=0, image_height=0, hide=False, limit_border=0):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.image = image
        self.image_width = image_width
        self.image_height = image_height
        self.hide = hide
        self.limit_border = limit_border
    
    def set_image(self, image_path, image_width, image_height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (image_width, image_height))
    
    def move(self):
        match (self.direction):
            case 'UP':    
                self.y -= self.speed
            case 'DOWN':
                self.y += self.speed
            case 'LEFT':
                self.x -= self.speed
            case 'RIGHT':
                self.x += self.speed
    
    def show(self, screen):
       if not self.hide:
           screen.blit(self.image, (self.x, self.y))