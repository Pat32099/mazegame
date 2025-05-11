from pygame import *
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Catch up")
background = transform.scale(image.load("background.jpg"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image , player_x, player_y , player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (70, 70))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"
        
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

playermain = Player('hero.png', 5, win_height - 80, 5)
entity = Enemy('cyborg.png', win_width - 80, 280, 3)
reward = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 20, 10, 350)
w3 = Wall(154, 205, 50, 100, 450, 350, 10)
w4 = Wall(154, 205, 50, 200, 110, 10, 350)
w5 = Wall(154, 205, 50, 300, 20, 10, 350)
w6 = Wall(154, 205, 50, 400, 110, 50, 350)
w7 = Wall(154, 205, 50, 400, 110, 150, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')

font.init()
font = font.Font(None,70)
win = font.render('WIN',True,(255,215,0))
lose = font.render('LOSE',True,(255,35,10))

game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        window.blit(background,(0, 0))
        playermain.update()
        entity.update()

        entity.reset()
        playermain.reset()
        reward.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()

        if sprite.collide_rect(playermain, reward):
            finish = True
            money.play()
            window.blit(win,(300,200))

        if sprite.collide_rect(playermain, entity) or sprite.collide_rect(playermain, w1):
            finish = True
            kick.play()
            window.blit(lose,(300,200))
            

 
    
    display.update()
    clock.tick(FPS)



