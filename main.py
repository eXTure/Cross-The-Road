#Basic cross the road game using pygame

import sys
import pygame
import os, logging

logging.basicConfig(level=logging.DEBUG,
                filename='app.log',
                filemode='w',
                format='%(name)s - %(levelname)s - %(message)s')

logging.info("Logging Test")
os.environ['SDL_VIDEO_CENTERED'] = "1" #Centers game window in the middle of the screen
SCREEN_WIDHT = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Cross The Road"
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

    def scores(self, player_name, score):

        self.player_name = player_name
        self.score = score

        execution_path = os.getcwd()
        f = open('highscore.txt','a')
        write_msg = player_name, ", ", str(score), "\n"
        f.writelines(write_msg)
        f.close()


    def scoring(self, level_number, level_speed):

        score_points = (level_number + level_speed) * 100

        return score_points


    def run_game_loop(self, level_speed, level_number, player_name):

        is_game_over = False
        did_win = False
        direction = 0
        self.player_name = player_name

        player_character = PlayerCharacter("images/player.png", 375, 700, 50, 50)

        enemy_0 = NonPlayerCharacter("images/enemy.png", 20, 600, 50, 50)
        enemy_0.SPEED *= level_speed

        enemy_1 = NonPlayerCharacter("images/enemy.png", self.width - 50, 400, 50, 50)
        enemy_1.SPEED *= level_speed

        enemy_2 = NonPlayerCharacter("images/enemy.png", 20, 200, 50, 50)
        enemy_2.SPEED *= level_speed

        treasure = GameObject("images/treasure.png", 375, 25, 50, 50)

        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN: #Event, when key is pressed
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_SPACE:
                        #Display score on the screen when player press space button
                        text = font.render("Your Score: "+str(int(self.scoring(level_number, level_speed))), True, WHITE_COLOR)
                        self.game_screen.blit(text, (200, 300))
                        pygame.display.update()
                        clock.tick(1)
                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        text = font.render("This won't help you run faster!", True, WHITE_COLOR)
                        self.game_screen.blit(text, (25, 325))
                        pygame.display.update()
                        clock.tick(1)
                    elif event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                elif event.type == pygame.KEYUP: #Event, when key is released
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

                #logging.info(event) print all movements and key presses to the terminal

            self.game_screen.fill(WHITE_COLOR) #Redraw the background image
            self.game_screen.blit(self.image, (0, 0))
            treasure.draw(self.game_screen)
            player_character.move(direction, self.height)
            player_character.draw(self.game_screen)
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level_number > 4: #Increasing difficulty
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)

            if level_number == 4: #Slow down speed when additional enemy appears
                level_speed = 1

            if level_number > 8: #Increasing difficulty
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            if level_number == 8: #Slow down speed when additional enemy appears
                level_speed = 1

            if player_character.detect_collision(enemy_0) == True:
                is_game_over = True
                did_win = False
                text = font.render("You lost! Try again.", True, BLACK_COLOR)
                self.game_screen.blit(text, (150, 300))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render("You Win!", True, WHITE_COLOR)
                self.game_screen.blit(text, (275, 300))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(enemy_1) == True:
                is_game_over = True
                did_win = False
                text = font.render("You lost! Don't rush!.", True, BLACK_COLOR)
                self.game_screen.blit(text, (150, 300))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(enemy_2) == True:
                is_game_over = True
                did_win = False
                text = font.render("You lost! Almost there!.", True, BLACK_COLOR)
                self.game_screen.blit(text, (150, 300))
                pygame.display.update()
                clock.tick(1)
                break

            pygame.display.update() #updates all game graphics
            clock.tick(self.TICK_RATE)

        if did_win:
            self.run_game_loop(level_speed + 0.5, level_number + 1, self.player_name)
        else:
            self.scores(player_name, int(self.scoring(level_number, level_speed)))
            self.run_game_loop(1, 1, self.player_name)


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

    def detect_collision(self, another_entity):
        """Check if there's a collision with another entity"""
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


if __name__ == "__main__":
    pygame.init()

    new_game = Game("images/background.png", SCREEN_TITLE, SCREEN_WIDHT, SCREEN_HEIGHT)
    score_points = 0
    player_name = input("Enter your name:")
    new_game.run_game_loop(1, 1, player_name)

    pygame.quit()
    quit()
