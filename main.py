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
track_width = track.get_width() -3
#track_rect = track.get_rect()
#track_rect.center = (0,335)


def draw_bg():
    screen.fill(BG)
    screen.blit(track, (floor_x_pos, 325))
    screen.blit(track, (floor_x_pos + track_width, 325))

class Manusia(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y,scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #load images 
        animation_type = ['Diam', 'Lari', 'Lompat', 'Mati']
        for animation in animation_type:
            #reset temporary list
            temp_list = []
            #count number of files
            num_of_frames = len(os.listdir(f'gambar/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'gambar/{self.char_type}/{animation}/{i}.png')
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
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy >335:
            dy = 335 - self.rect.bottom
            self.in_air = False


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
floor_x_pos = 0
game_speed = 5

while run:

    floor_x_pos -= 1
    draw_bg()
    if floor_x_pos <= -track_width:
        floor_x_pos = 0
    floor_x_pos -= game_speed

    clock.tick(FPS)

    pemain.update_animation()
    pemain.draw()
    kerumunan.draw()

    #update player action
    if pemain.alive:
        if pemain.in_air:
            pemain.update_action(2)#lompat
        elif walk:
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
