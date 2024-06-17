import pygame
from pygame.locals import *
import time
import random



class Bird:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/bird.png")
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 300
        self.direction = 'down'


    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))


    def flap(self):
        self.y -= 100

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        if self.direction == 'down':
            if self.y <= 631:
                if self.y <= 50:
                    self.y *= 1.1
                elif self.y <= 200:
                    self.y *= 1.01
                else:
                    self.y *= 1.003

        self.draw()

    
    
class Tubesr:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/tubesr.png")
        self.parent_screen = parent_screen
        self.x = 1000
        self.y = -700
        self.direction = 'left'

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def walk(self):
        if(self.x > -250):
            if self.direction == 'left':
                self.x -= 4
        else:
            self.x = 1000
        self.draw()


class Tubes:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/tubes.png")
        self.parent_screen = parent_screen
        self.x = 1000
        self.y = 500
        self.direction = 'left'
        self.count = 0

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))


    def walk(self):
        if(self.x > -250):
            if self.direction == 'left':
                self.x -= 4
        else:
            self.x = 1000
            self.count += 1
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_bg_music()
        self.surface = pygame.display.set_mode((1024, 768))
        self.tubes = Tubes(self.surface)
        self.tubes.draw()
        self.tubesr = Tubesr(self.surface)
        self.tubesr.draw()
        self.bird = Bird(self.surface)
        self.bird.draw()


    def is_collision(self, x1, y1, x2, y2, y3):
        if x1 >= x2 and ((x1 < x2 + 200) or (x1 < x2 - 200)):
            if (y1 <= 215) or (y1 >= 425):
                return True

    def render_bg(self):
        bg = pygame.image.load("resources/bg1024x768.webp")
        self.surface.blit(bg, (0,0))


    def play_bg_music(self):
        pygame.mixer.music.load("resources/music.mp3")
        pygame.mixer.music.play()


    def play(self):
        self.render_bg()
        self.tubes.walk()
        self.tubesr.walk()
        self.bird.walk()
        self.bird.draw()
        self.tubes.draw()
        self.tubesr.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.bird.x, self.bird.y, self.tubes.x, self.tubes.y, self.tubesr.y):
            raise "Game over"

        
    

    def show_game_over(self):
        self.render_bg()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.tubes.count}", True, (255,255,255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again press Enter. To exit press Escape!", True, (255,255,255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()
        sound1 = pygame.mixer.Sound("resources/dead.mp3")
        pygame.mixer.Sound.play(sound1)



    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.tubes.count}", True, (255,255,255))
        self.surface.blit(score, (800, 10))


    def reset(self):
        self.tubes = Tubes(self.surface)
        self.tubesr = Tubesr(self.surface)
        self.bird = Bird(self.surface)

    def run(self):
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        
                    if event.key == K_RETURN:
                        paused = False
                        pygame.mixer.music.unpause()
                    if not paused:
                        if event.key == K_UP:
                            self.bird.flap()

                elif event.type == QUIT:
                        running = False
            try:
                if not paused:
                    self.play()
            except Exception as e:
                self.show_game_over()
                paused = True
                self.reset()



if __name__ == '__main__':
    game = Game()
    game.run()