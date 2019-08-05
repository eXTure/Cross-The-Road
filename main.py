#Basic cross the road game using pygame

import sys
import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = "1"
SCREEN_WIDHT = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Cross The Road RPG"
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("comicsans", 75)

class Game:

    TICK_RATE = 60 #Frame rate for the game

    def __init__(self, image_path, title, width, height):

        self.title = title
        self.width = width
        self.height = height

        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level):

        is_game_over = False
        did_win = False
        direction = 0
        player_character = PlayerCharacter("player.png", 375, 700, 50, 50)

        enemy_0 = NonPlayerCharacter("enemy.png", 20, 600, 50, 50)
        enemy_0.SPEED *= level

        enemy_1 = NonPlayerCharacter("enemy.png", self.width - 50, 400, 50, 50)
        enemy_1.SPEED *= level

        enemy_2 = NonPlayerCharacter("enemy.png", 20, 200, 50, 50)
        enemy_2.SPEED *= level

        treasure = GameObject("treasure.png", 375, 25, 50, 50)

        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN: #Event, when key is pressed
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                elif event.type == pygame.KEYUP: #Event, when key is released
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            print(event)

            self.game_screen.fill(WHITE_COLOR) #Redraw the background image
            self.game_screen.blit(self.image, (0, 0))
            treasure.draw(self.game_screen)
            player_character.move(direction, self.height)
            player_character.draw(self.game_screen)
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level > 2: #Increasing difficulty
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level > 4:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            if player_character.detect_collision([enemy_0, enemy_1, enemy_2]) == True:
                is_game_over = True
                did_win = False
                text = font.render("You lost! Try again.", True, BLACK_COLOR)
                self.game_screen.blit(text, (150, 300))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision([treasure]):
                is_game_over = True
                did_win = True
                text = font.render("You Win!", True, WHITE_COLOR)
                self.game_screen.blit(text, (275, 300))
                pygame.display.update()
                clock.tick(1)
                break

            pygame.display.update() #updates all game graphics
            clock.tick(self.TICK_RATE)

        if did_win:
            self.run_game_loop(level + 0.5)
        else:
            self.run_game_loop(1)
            #return


class GameObject:

    def __init__(self, image_path, x, y, width, height):
        """Path to image, coordinates on the screen, width and height of the object"""

        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

class PlayerCharacter(GameObject):
    """Character controled by a human player."""

    SPEED = 8

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height):
        if direction > 0: #Positive direction moves character downwards
            self.y_pos -= self.SPEED
        elif direction < 0: #Negative values moves character upwards
            self.y_pos += self.SPEED

        if self.y_pos >= max_height - 50:
            self.y_pos = max_height - 50
        elif self.y_pos <= 0:
            self.y_pos = 0

    def detect_collision(self, another_entity_list):
        """Check if there's a collision with another entity"""
        for another_entity in another_entity_list:
            if self.y_pos > another_entity.y_pos + another_entity.height:
                return False
            elif self.y_pos + self.height < another_entity.y_pos:
                return False

            if self.x_pos > another_entity.x_pos + another_entity.width:
                return False
            elif self.x_pos + self.width < another_entity.x_pos:
                return False

            return True


class NonPlayerCharacter(GameObject):

    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):
        if self.x_pos <= 40:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 80:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED


pygame.init()

new_game = Game("background.png", SCREEN_TITLE, SCREEN_WIDHT, SCREEN_HEIGHT)
new_game.run_game_loop(1)

pygame.quit()
quit()
