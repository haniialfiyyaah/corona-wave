import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Corona Wave")

#framerate
clock = pygame.time.Clock()
FPS = 60


#define game variables
GRAVITY = 0.75

#player action
walk = False



#define colours
BG = (255,255,255)
track = pygame.image.load('gambar/background/Track.png')
track_rect = track.get_rect()
track_rect.center = (0,335)

def draw_bg():
    screen.fill(BG)
    screen.blit(track, track_rect)

class Manusia(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y,scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.vel_y = 0
        self.jump = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'gambar/{self.char_type}/Diam/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'gambar/{self.char_type}/Lari/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def move(self):
        dx = 0
        dy = 0

        #jump
        if self.jump == True:
            self.vel_y = -11
            self.jump = False

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy >335:
            dy = 335 - self.rect.bottom


        #update rect position
        self.rect.x += dx
        self.rect.y += dy


    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image
        self.image = self.animation_list[self.action][self.frame_index] 
        #check time
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        #reset animation
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        #check action
        if new_action != self.action:
            self.action = new_action
            #update animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(self.image, self.rect)    

pemain = Manusia('pemain',125,300,2,5)
kerumunan = Manusia('kerumunan',200,300,2,5)

run = True

while run:

    clock.tick(FPS)

    draw_bg()

    pemain.update_animation()
    pemain.draw()
    kerumunan.draw()

    #update player action
    if pemain.alive:
        if walk:
            pemain.update_action(1)#1: lari
        else:
            pemain.update_action(0)#0: diam
        pemain.move()

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and pemain.alive:
                pemain.jump = True
                walk = True

        #keyboard release



    pygame.display.update()


pygame.quit()
