import pygame
import time
import random
import tkinter as tk
from tkinter import simpledialog

pygame.init()

# Определение цветов
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 - mesg.get_height() / 2])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def gameLoop(snake_speed):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Загрузка максимального счета пользователя из файла
    try:
        with open('snake_highscore.txt', 'r') as f:
            highscore = int(f.read())
    except FileNotFoundError:
        highscore = 0

    while not game_over:

        while game_close:
            if Length_of_snake - 1 > highscore:
                highscore = Length_of_snake - 1
                with open('snake_highscore.txt', 'w') as f:
                    f.write(str(highscore))

            dis.fill(blue)
            message(f"Вы проиграли! Ваш текущий счет: {Length_of_snake - 1}. Максимальный счет: {highscore}."
                    f" Нажмите C-начать Q-выйти", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(snake_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        # Отображение текущего счета
        score = score_font.render(f"Счет: {Length_of_snake - 1}", True, black)
        dis.blit(score, (10, 10))

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


def get_settings():
    root = tk.Tk()
    root.withdraw()
    speed = simpledialog.askinteger("Скорость змейки", "Выберите скорость змейки (от 10 до 50):", minvalue=10, maxvalue=50)
    width = simpledialog.askinteger("Ширина экрана", "Введите ширину окна (в пикселях):")
    height = simpledialog.askinteger("Высота экрана", "Введите высоту окна (в пикселях):")
    return speed, width, height


# Получение настроек игры от пользователя
snake_speed, dis_width, dis_height = get_settings()

# Инициализация окна
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка игра')

# Определение размера блока змейки
snake_block = 10

# Определение часов
clock = pygame.time.Clock()

# Запуск игры с передачей скорости змейки
gameLoop(snake_speed)
