# BOIDS
'''
    Read about boids here - https://en.wikipedia.org/wiki/Boids
    Created by https://chief141.github.io

    Side Note - I have highlighted one boid to make it easy to follow
'''

import pygame
from sys import exit
from random import randint, uniform, choice

WIDTH = 800
HEIGHT = 600
fps = 30

black = (0,0,0)
white = (255,255,255)

#for display
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BOIDs")
clock = pygame.time.Clock()

def draw_text(surf,text,size,x,y,color=white):
    font_name=pygame.font.match_font('aerial')
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.center=(x,y)
    surf.blit(text_surface,text_rect)

MAX_SPEED = 8
BOID_COLOR = (255,255,56)
SPECIAL_BOID_COLOR = (255, 10 ,10)
BOID_SIZE = 8

FLEE_RADIUS = 43
MAX_FLEE_FORCE = 22

ALIGN_RADIUS = 120

COHESION_RADIUS = 400

vec = pygame.math.Vector2
#MAIN CLASS BOIDS
class Boid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BOID_SIZE,BOID_SIZE))
        self.image.fill(BOID_COLOR)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = vec(choice([-MAX_SPEED, MAX_SPEED]),choice([-MAX_SPEED, MAX_SPEED])).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    #UPDATE FUNCTION
    def update(self):
        self.acc = vec(0,0)
        for i in boids:
            if i != self:
                self.acc += self.separation(i.rect.center)
        self.acc += self.alignment()
        self.acc += self.cohesion()

        self.vel += (self.acc * DELTA_TIME)

        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel

        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.y > HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = HEIGHT


        self.rect.center = self.pos

    def separation(self, target):
        '''
        Function for Rule 1 - Separation
        Steer to avoid crowding local flockmates
        '''

        steer = vec(0,0)
        dist = self.pos - target
        desired = vec(0,0)

        if dist.x != 0 and dist.y != 0 :
            if dist.length() < FLEE_RADIUS:
                desired = dist.normalize() * MAX_SPEED
            else:
                desired = self.vel.normalize() * MAX_SPEED
        steer = desired - self.vel
        if steer.length() > MAX_FLEE_FORCE:
            steer.scale_to_length(MAX_FLEE_FORCE)
        return steer

    def alignment(self):
        '''
        Function for Rule 2 - Alignment
        Steer towards the average heading of local flockmates
        '''

        align = vec(0,0)
        desired = vec(0,0)
        for i in boids:
            if i != self:
                if i.vel.x != 0 and i.vel.y != 0:
                    if (self.pos - i.pos).length() < ALIGN_RADIUS:
                        desired += i.vel.normalize() * MAX_SPEED

        align = desired - self.vel
        align =  align // (len(boids))

        if align.length() > MAX_SPEED:
            align.scale_to_length(MAX_SPEED)

        return align

    def cohesion(self):
        '''
        Function for Rule 3 - Cohesion
        Steer to move towards the average position (center of mass) of local flockmates
        '''
        cohes = vec(0,0)
        average_location = vec(0,0)
        for i in boids:
            if i != self:
                dist = self.pos - i.pos
                if dist.length() < COHESION_RADIUS:
                    average_location += i.pos

        average_location = average_location/(len(boids) - 1)
        cohes = average_location - self.pos
        cohes = cohes.normalize() * MAX_SPEED
        return cohes


def create_boids(number):
    global all_sprite, boids
    #sprite groups
    all_sprite = pygame.sprite.Group()

    #OBJECTS
    boids = [Boid() for _ in range(number)]
    boids[0].image.fill(SPECIAL_BOID_COLOR)
    all_sprite.add(boids)

create_boids(10)

#game loop
no = 10
run = True
last_click = pygame.time.get_ticks()
while run:
    #clock spped
    DELTA_TIME = clock.tick(fps)/1000

    a,b,c = pygame.mouse.get_pressed()
    if a:
        if pygame.time.get_ticks() - last_click >= 400:
            last_click = pygame.time.get_ticks()
            create_boids(10 + no)
            no += 10

    #input(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update
    all_sprite.update()

    #Draw/render
    screen.fill(black)
    all_sprite.draw(screen)
    if no <= 20:
        draw_text(screen, "Left click to increase Boids",25, WIDTH/2, 20)
    pygame.display.flip()

pygame.quit()
exit()