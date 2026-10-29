from pygame import *
font.init()
scr = display.set_mode((700, 400))
scr.fill((255, 255, 255))
clock = time.Clock()
class Stuff(sprite.Sprite):
    def __init__(self, ex, l, w, speed, x, y):
        super().__init__()
        self.ex = transform.scale(image.load(ex), (l, w))
        self.speed = speed
        self.rect = self.ex.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self, x, y):
        scr.blit(self.ex, (self.rect.x, self.rect.y))
class Players(Stuff):
    def __init__(self, ex, l, w, speed, x, y, key1, key2):
        super().__init__(ex, l, w, speed, x, y)
        self.key1 = key1
        self.key2 = key2
    def control(self):
        keys = key.get_pressed()
        if keys[self.key2] and self.rect.y < 300:
            self.rect.y += self.speed
        if keys[self.key1] and self.rect.y > 1:
            self.rect.y -= self.speed
class Ball(Stuff):
    def __init__(self, ex, l, w, speed, x, y, speed2):
        super().__init__(ex, l, w, speed, x, y)
        self.speed2 = speed2
    def move(self):
        self.rect.x += self.speed
        self.rect.y += self.speed2
        if self.rect.x <= 0:
            global wn_con
            wn_con = font.render('P1 (LEFT) lost', True, (230, 0, 0))
            col = (255, 0, 0)
            finish = True
        if self.rect.x >= 650:
            wn_con = font.render('P2 (RIGHT) lost', True, (0, 240, 0))
            col = (0, 255, 0)
            finish = True
        if self.rect.y <= 0:
            self.speed2 *= -1
            self.rect.y = 5
        if self.rect.y >= 380:
            self.speed2 *= -1
            self.rect.y = 377
        
    def collision(self):
        if self.rect.colliderect(player1) or self.rect.colliderect(player2):
            if self.rect.colliderect(player1):
                self.rect.x += 10
            elif self.rect.colliderect(player2):
                self.rect.x -= 10
            self.speed *= -1
font = font.Font(None, 85)
col = None
wn_con = None
ball = Ball('rocket.png', 30, 30, 5, 350, 200, 5)
player1 = Players('asteroid.png', 20, 100, 3, 100, 200, K_w, K_s)
player2 = Players('asteroid.png', 20, 100, 3, 600, 200, K_UP, K_DOWN)
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        if ball.rect.x <= 0:
            col = (255, 0, 0)
            finish = True
        if ball.rect.x >= 650:
            col = (0, 255, 0)
            finish = True
        player1.control()
        player2.control()
        ball.move()
        ball.collision()
        scr.fill((200, 255, 255))
        ball.draw(0, 0)
        player1.draw(0, 0)
        player2.draw(0, 0)
    else:
        scr.fill(col)
        scr.blit(wn_con, (200, 300))
        display.update()
    clock.tick(60)
    display.update()