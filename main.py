import pygame
import sys
from pygame import Surface

pygame.init()

window_size = (700, 500)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Maze")

fps = 60

clock = pygame.time.Clock()

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, window_size)

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(GameSprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.x < 725 - 86:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.y < 550 - 96:
            self.rect.y += 5

class Enemy(GameSprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.direction = -0.8
        self.timer = 0
        self.move_duration = 1.8 * fps

    def update(self):
        self.timer += 1
        if self.timer >= self.move_duration:
            self.direction *= -1
            self.timer = 0
        self.rect.x += self.direction * 2

class Enemy_v(GameSprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.direction = -0.8
        self.timer = 0
        self.move_duration = 3 * fps

    def update(self):
        self.timer += 1
        if self.timer >= self.move_duration:
            self.direction *= -1
            self.timer = 0

        self.rect.y += self.direction * 2

class Wall(pygame.sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_1, self.color_2, self.color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

class Treasure(GameSprite):
    def __init__(self, x, y):
        super().__init__(pygame.image.load("treasure.png"), x, y)

font = pygame.font.Font(None, 36)
win_text = font.render("YOU WIN!", True, (0, 255, 0))
lose_text = font.render("YOU LOSE!", True, (255, 0, 0))

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
treasures = pygame.sprite.Group()

w1 = Wall(154,205,50,0,230,200,10)
w2 = Wall(154,205,50,0,300,200,10)
w3 = Wall(154,205,50,100,135,200,10)
w4 = Wall(154,205,50,152,287,325,10)
w5 = Wall(154,205,50,195,30,475,10)
w6 = Wall(154,205,50,310,130,235,10)
w7 = Wall(154,205,50,540,160,250,10)
w8 = Wall(154,205,50,465,205,160,10)
w9 = Wall(154,205,50,390,370,160,10)
w10 = Wall(154,205,50,390,280,160,10)
w11 = Wall(154,205,50,335,325,100,10)
w12 = Wall(154,205,50,128,372,155,10)
w13 = Wall(154,205,50,200,445,110,10)

w3.angle = 90
w3.image = pygame.transform.rotate(w3.image, w3.angle)
w3.rect = w3.image.get_rect(center=w3.rect.center)

w4.angle = 90
w4.image = pygame.transform.rotate(w4.image, w4.angle)
w4.rect = w4.image.get_rect(center=w4.rect.center)

w7.angle = 90
w7.image = pygame.transform.rotate(w7.image, w7.angle)
w7.rect = w7.image.get_rect(center=w7.rect.center)

w8.angle = 90
w8.image = pygame.transform.rotate(w8.image, w8.angle)
w8.rect = w8.image.get_rect(center=w8.rect.center)

w11.angle = 90
w11.image = pygame.transform.rotate(w11.image, w11.angle)
w11.rect = w11.image.get_rect(center=w11.rect.center)

w12.angle = 90
w12.image = pygame.transform.rotate(w12.image, w12.angle)
w12.rect = w12.image.get_rect(center=w12.rect.center)


treasure = Treasure(350, 400)

all_sprites.add(w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,treasure)
walls.add(w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13)
treasures.add(treasure)
enemies = pygame.sprite.Group()

player = Player(pygame.image.load("player.png"), 15, 250)
enemy = Enemy(pygame.image.load("enemy.png"), 600, 300)
enemy2 = Enemy_v(pygame.image.load("enemy2.png"), 220, 400)

enemies.add(enemy,enemy2)

all_sprites.add(player, enemies)

running = True
game_over = False
game_over_text = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        all_sprites.update()

        if pygame.sprite.spritecollide(player, walls, False):
            game_over = True
            game_over_text = lose_text
            pygame.mixer.Sound("lose_sound.mp3").play()

        if pygame.sprite.spritecollide(player, treasures, True):
            game_over = True
            game_over_text = win_text
            pygame.mixer.Sound("win_sound.mp3").play()

        if pygame.sprite.spritecollide(player,enemies, False):
            game_over = True
            game_over_text = lose_text
            pygame.mixer.Sound("lose_sound.mp3").play()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    if game_over_text:
        screen.blit(game_over_text, (350,200))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()