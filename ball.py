from game_object import GameObject
import math

class Ball(GameObject):
    def __init__(self, x=0, y=0, speed=0, direction='UP', image=None, image_width=0, \
        image_height=0, hide=False, limit_border=0, power=0, curve_amount=0, kick_x=0):
        super().__init__(x, y, speed, direction, image, image_width, image_height, hide, limit_border)
        self.curve_left = False
        self.curve_right = False
        self.power = power
        self.curve_amount = curve_amount
        self.kick_x = kick_x
        
    def move(self):
        super().move()
        match (self.direction):
            case 'UP':   
                #additional increment for power shot
                self.y -= self.power
                if self.curve_left:
                    if self.y > 0:
                        # self.x = self.curve_amount*math.sqrt(48400 - pow(self.y - 220, 2)) + self.kick_x
                        self.x = -(440/(12*self.y+75)) + self.x
                if self.curve_right:
                    if self.y > 0:
                        # self.x = self.curve_amount*math.sqrt(48400 + pow(self.y - 220, 2)) + self.kick_x
                        self.x = (440/(12*self.y+75)) + self.x


        
        
        


        