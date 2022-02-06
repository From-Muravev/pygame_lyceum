import os
import sys
import pygame
import random
from random import randint
from models.ball import Ball
from models.pad import Pad
from models.score import Score
import datetime

width, height = 800, 600
BACkGROUND_COLOR = (0, 0, 0)
SCREEN_SIZE = width, height
INTRO1_TEXT_POS = (260, 20)
INTRO2_TEXT_POS = (340, 100)
MENU_POS1 = (325, 320)
MENU_POS2 = (325, 390)
MENU_POS3 = (325, 460)
MENU_MPOS = (300, 220)

fps = 60

pygame.init()
size = SCREEN_SIZE
screen = pygame.display.set_mode(size)
font_1 = pygame.font.Font(None, 80)
font_2 = pygame.font.Font(None, 40)


def rules():
    clock = pygame.time.Clock()
    intro_text = ["Space: Start ball",
                  "W and S: Control left player",
                  "Up arrow and Down arrow: Control right player"]
    screen.fill(BACkGROUND_COLOR)
    printcFont(font_1, "Rules for play", (220, 20), (255, 255, 255))
    text_coord = 150
    for line in intro_text:
        string_rendered = font_2.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return start_screen()
        pygame.display.flip()
        clock.tick(fps)

def terminate():
    pygame.quit()
    sys.exit()


def printcFont(font, message, vect, color):
    screen.blit(font.render(message, True, color), vect)


def update_colors():
    color = (randint(10, 255), randint(10, 255), randint(10, 255))
    printcFont(font_1, 'Atari Pong', INTRO1_TEXT_POS, color)
    printcFont(font_1, '1972', INTRO2_TEXT_POS, color)


def start_screen():
    clock = pygame.time.Clock()
    screen.fill(BACkGROUND_COLOR)
    color = (randint(10, 255), randint(10, 255), randint(10, 255))
    printcFont(font_1, 'Atari Pong', INTRO1_TEXT_POS, color)
    printcFont(font_1, '1972', INTRO2_TEXT_POS, color)
    printcFont(font_2, 'Enter:  Play', MENU_POS1, (255, 255, 255))
    printcFont(font_2, 'Escape: Exit', MENU_POS3, (255, 255, 255))
    printcFont(font_2, 'Space:  Rules', MENU_POS2, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return main()
                elif event.key == pygame.K_ESCAPE:
                    return terminate()
                elif event.key == pygame.K_SPACE:
                    return rules()
        pygame.display.flip()
        clock.tick(fps)
        if clock.tick(60000):
            update_colors()


def main():
    pygame.display.set_caption('Pong')
    try:
        filename = os.path.join('assets', 'graphics', 'background.png')
        background = pygame.image.load(filename)
        background = background.convert()

    except pygame.error as e:
        raise SystemExit(str(e))
    pad_left = Pad((width / 6, height / 4))
    pad_right = Pad((5 * width / 6, 3 * height / 4))
    ball = Ball((width / 2, height / 2))
    if not pygame.font:
        raise SystemExit('Pygame does not support fonts')

    try:
        filename = os.path.join('assets', 'fonts', 'wendy.ttf')
        font = pygame.font.Font(filename, 90)

    except pygame.error as e:
        raise SystemExit(str(e))

    left_score = Score(font, (width / 3, height / 8))
    right_score = Score(font, (2 * width / 3, height / 8))
    sprites = pygame.sprite.Group(pad_left, pad_right, ball, left_score, right_score)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,
                          1000 // fps)
    top = pygame.Rect(0, 0, width, 5)
    bottom = pygame.Rect(0, height - 5, width, 5)
    left = pygame.Rect(0, 0, 5, height)
    right = pygame.Rect(width - 5, 0, 5, height)

    while 1:
        clock.tick(fps)
        pad_left.stop()
        pad_right.stop()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            pad_left.move_up()

        if keys[pygame.K_s]:
            pad_left.move_down()

        if keys[pygame.K_UP]:
            pad_right.move_up()

        if keys[pygame.K_DOWN]:
            pad_right.move_down()

        if keys[pygame.K_SPACE] and ball.isStopped():
            ball.start(random.choice([-1, 1]) * randint(1, 4), random.choice([-1, 1]) * randint(1, 4))

        if keys[pygame.K_ESCAPE]:
            terminate()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if ball.rect.colliderect(top) or ball.rect.colliderect(bottom):
            ball.change_y()
        elif (ball.rect.colliderect(pad_left.rect) or ball.rect.colliderect(pad_right.rect)):
            ball.change_x()
        elif ball.rect.colliderect(left):
            right_score.score_up()
            ball.reset()
            ball.stop()
        elif ball.rect.colliderect(right):
            left_score.score_up()
            ball.reset()
            ball.stop()

        screen_rect = screen.get_rect().inflate(0, -10)
        pad_left.rect.clamp_ip(screen_rect)
        pad_right.rect.clamp_ip(screen_rect)

        sprites.update()
        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    os.system("cls")  # Clear console
    print("Start: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start_screen()
    # main()
    print("End: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
