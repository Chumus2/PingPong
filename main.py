import pygame
import time

pygame.init()
pygame.font.init()

# Class for the players (walls)
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)  # Create rectangle
        self.color = color
        self.speed = 5

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # Draw rectangle

    def move_up(self):  # Moving up
        if self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed

    def move_down(self, window_height):  # Moving down
        if self.rect.y + self.rect.height + self.speed <= window_height:
            self.rect.y += self.speed

# Class for the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed_x, speed_y, sprite):
        super().__init__()
        self.image = pygame.image.load(sprite)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def draw(self, surface):  # Draw
        surface.blit(self.image, self.rect)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = -self.speed_y
        elif self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.speed_y = -self.speed_y
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x = -self.speed_x
        elif self.rect.right >= 600:
            self.rect.right = 600
            self.speed_x = -self.speed_x

    def collides(self, walls):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.rect.right > wall.rect.left and self.rect.left < wall.rect.left:
                    self.rect.right = wall.rect.left
                    self.speed_x = -self.speed_x
                elif self.rect.left < wall.rect.right and self.rect.right > wall.rect.right:
                    self.rect.left = wall.rect.right
                    self.speed_x = -self.speed_x

                if self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top:
                    self.rect.bottom = wall.rect.top  
                    self.speed_y = -self.speed_y
                elif self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom  
                    self.speed_y = -self.speed_y

# Function to reset the game
def reset_game():
    global ball, player1, player2, game_over, result_text
    ball = Ball(265, 200, 75, 75, -4, 2, 'ball.png')  # Ball
    player1 = Wall(25, 150, 25, 150, (129, 219, 206))  # First player
    player2 = Wall(550, 150, 25, 150, (129, 219, 206))  # Second player
    result_text = ''
    players.empty()
    players.add(player1)
    players.add(player2)
    game_over = False

# Window setup
window = pygame.display.set_mode((600, 500))  # Size
pygame.display.set_caption('PingPong')
background = pygame.image.load('bg.png')  # Background
background = pygame.transform.scale(background, (600, 500))

# Create ball, players and other
ball = Ball(265, 200, 75, 75, -4, 2, 'ball.png')  # Ball
player1 = Wall(25, 150, 25, 150, (129, 219, 206))  # First player
player2 = Wall(550, 150, 25, 150, (129, 219, 206))  # Second player

font1 = pygame.font.SysFont('Arial', 50)  # Font1
font2 = pygame.font.SysFont('Arial', 25)  # Font2

# Sprite group
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

# Game loop
clocks = pygame.time.Clock()
game = True
game_over = False
result_text = ''

while game:
    for e in pygame.event.get(): 
        if e.type == pygame.QUIT:  # Quit button
            game = False
    
    if not game_over:
        keys = pygame.key.get_pressed()  # Check any keys 
        if keys[pygame.K_UP]:  # Moving up
            player1.move_up()
        if keys[pygame.K_DOWN]:  # Moving down
            player1.move_down(500)
        if keys[pygame.K_w]:  # Moving up
            player2.move_up()
        if keys[pygame.K_s]:  # Moving down
            player2.move_down(500)

        ball.move()
        
        # Ball collisions
        if ball.rect.left <= 0:  # Collide with wall1
            game_over = True
            result_text = 'Player1 Loses!'
        elif ball.rect.right >= 600:  # Collide with wall2
            game_over = True
            result_text = 'Player2 Wins!'

        # Check collisions with players
        ball.collides(players)

        # Draw all
        window.blit(background, (0, 0))
        player1.draw(window)
        player2.draw(window)
        ball.draw(window)
        
        #game_over
        if game_over:
            if result_text == 'Player2 Wins!':
                result = font1.render(result_text, True, (0, 255, 0))
            elif result_text == 'Player1 Loses!':
                result = font1.render(result_text, True, (255, 0, 0))
            restart_text = font2.render('Press R to restart', True, (255, 255, 255))
            window.blit(restart_text, (180, 300))
            window.blit(result, (160, 225))

            #Restart
            keys1 = pygame.key.get_pressed()
            if keys1[pygame.K_r]:  # Restart button
                reset_game()

    else:
        keys1 = pygame.key.get_pressed()
        if keys1[pygame.K_r]:  # Restart button
            reset_game()

    clocks.tick(60)
    pygame.display.update()
