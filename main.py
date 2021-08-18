import pygame
import os
import random
import threading
from threading import Timer

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Corona Wave")

icon = pygame.image.load('gambar/virus/1.png')
pygame.display.set_icon(icon)

# framerate
clock = pygame.time.Clock()
FPS = 60


# define game variables
GRAVITY = 0.5

# player action
walk = False


# obstacle
VIRUS = [pygame.image.load(os.path.join('gambar/virus', '0.png')),
         pygame.image.load(os.path.join('gambar/virus', '1.png'))]

ORANG_DOUBLE = [pygame.image.load(os.path.join('gambar/orang', 'double1.png')),
                pygame.image.load(os.path.join('gambar/orang', 'double2.png'))]

ORANG_SINGLE = [pygame.image.load(os.path.join('gambar/orang', 'single1.png')),
                pygame.image.load(os.path.join('gambar/orang', 'single2.png'))]

VAKSIN = [pygame.image.load(os.path.join('gambar/vaksin', 'vaksin.png')),
          pygame.image.load(os.path.join('gambar/vaksin', 'vaksin.png'))]


# world
bg_img = pygame.image.load('gambar/background/bg1.png')
bg_width = bg_img.get_width()
track = pygame.image.load('gambar/background/track2.png')
track_width = track.get_width()
trophy = pygame.image.load('gambar/trophy.png')


#menu
start_menu = pygame.image.load('gambar/menu/start_menu.png')
restart_menu = pygame.image.load('gambar/menu/restart.png')
win = pygame.image.load('gambar/menu/win.png')

class Manusia(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
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

        self.protected = False

        # load images
        animation_type = ['Diam', 'Lari', 'Lompat', 'Kebal', 'Jump']
        for animation in animation_type:
            # reset temporary list
            temp_list = []
            # count number of files
            num_of_frames = len(os.listdir(
                f'gambar/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'gambar/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        dx = 0
        dy = 0

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 405:
            dy = 405 - self.rect.bottom
            self.in_air = False

        # update rect position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check time
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset animation
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check action
        if new_action != self.action:
            self.action = new_action
            # update animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)


class Obstacle:

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Virus1(Obstacle):

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 285
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


class Virus2(Obstacle):

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 340
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


class Orang(Obstacle):

    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 335


class Power:

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            powers.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Vaksin(Power):

    def __init__(self, image):
        self.type = 0
        # img = pygame.transform.scale(
        #     image, (int(image.get_width() * 5), int(image.get_height() * 5)))
        super().__init__(image, self.type)
        self.rect.y = 335

    # def draw(self, SCREEN):
    #     if self.index >= 9:
    #         self.index = 0
    #     SCREEN.blit(self.image[0], self.rect)
    #     self.index += 1


def main():
    global game_speed, bg_x_pos, floor_x_pos, points, obstacles, walk, powers
    run = True
    walk = True
    clock = pygame.time.Clock()
    pemain = Manusia('pemain', 125, 300, 2, 5)
    game_speed = 5
    bg_x_pos = 0
    floor_x_pos = 0
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    powers = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 500 == 0:
            game_speed += 1

        text = font.render('Poin: ' + str(points), True, (0, 23, 158))
        textRect = text.get_rect()
        textRect.center = (700, 40)
        screen.blit(text, textRect)
        if points == 2000 or points == 7000: #limit vaksin
            pemain.protected = False

    def draw_bg():
        global bg_x_pos, floor_x_pos
        screen.blit(bg_img, (bg_x_pos, 0))
        screen.blit(bg_img, (bg_x_pos + bg_width, 0))
        screen.blit(bg_img, (bg_x_pos + bg_width*2, 0))
        screen.blit(track, (floor_x_pos, 405))
        screen.blit(track, (floor_x_pos + track_width, 405))
#        if walk:
        if bg_x_pos <= -(bg_width*2):
            bg_x_pos = 0
        bg_x_pos -= game_speed
        if floor_x_pos <= -track_width:
            floor_x_pos = 0
        floor_x_pos -= game_speed

    def changeProtected(val):
        pemain.protected = val


    while run:
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                run = False
            # keyboard press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER and pemain.alive:
                    walk = True
                if event.key == pygame.K_SPACE and pemain.alive:
                    pemain.jump = True

        draw_bg()
        clock.tick(FPS)
        pemain.draw()
        pemain.update_animation()

        # update player action
        if pemain.alive:
            if pemain.in_air and pemain.protected:
                pemain.update_action(4)  # lompat kebal
            elif pemain.protected:
                pemain.update_action(3)  # 3: kebal
            elif pemain.in_air:
                pemain.update_action(2)  # 3: lompat    
            elif walk:
                pemain.update_action(1)  # 1: lari
            else:
                pemain.update_action(0)  # 0: diam
            pemain.move()

            if len(obstacles) == 0 and points < 7300:
                if random.randint(0, 3) == 0:
                    obstacles.append(Orang(ORANG_SINGLE))
#                elif random.randint(0, 3) == 1:
#                    obstacles.append(Orang(ORANG_DOUBLE))
                elif random.randint(0, 3) == 2:
                    obstacles.append(Virus1(VIRUS))
                elif random.randint(0, 3) == 3:
                    obstacles.append(Virus2(VIRUS))



            if len(powers) == 0 and (points == 1000 or points == 3000):
#                if random.randint(0, 3) == 0:
                powers.append(Vaksin(VAKSIN))

            for obstacle in obstacles:
                obstacle.draw(screen)
                obstacle.update()
                if pemain.protected == False:
                    if pemain.rect.colliderect(obstacle.rect):
                        pygame.time.delay(1000)
                        death_count += 1
                        menu(death_count)

            for power in powers:
                power.draw(screen)
                power.update()
                if pemain.rect.colliderect(power.rect):                    
                    changeProtected(True)   

            if points == 7621: #Win end game
                pygame.time.delay(1000)
                death_count += 2
                menu(death_count)

        if points >= 7450:
            screen.blit(trophy,(400,335))
        
        score()
        pygame.display.update()


# pygame.quit()

def menu(death_count):
    global points, walk
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 20)

        if death_count == 0: #start menu
            text = font.render('', True, (0, 0,
                               0))
            screen.blit(start_menu,(0,0))  
        elif death_count == 1: #restart
            text = font.render('Anda Kalah ', True, (0, 23,
                               158))
            screen.blit(restart_menu,(0,0))
            score = font.render('Skor: ' + str(points), True, (0,
                                23, 158))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                                + 100)
            screen.blit(score, scoreRect)

        elif death_count > 1: #win
            text = font.render('', True, (255, 0,
                               0))
            screen.blit(win,(0,0))                               
            score = font.render('Skor: ' + str(points), True, (0,
                                23, 158))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                                + 40)
            screen.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
        screen.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
