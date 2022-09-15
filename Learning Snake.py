# Code to play the google snake game via an algorithm
import time
# imports
import webbrowser
import numpy as np
import cv2
import pyautogui
from PIL import Image
from pyautogui import Point
import threading
print(cv2.__version__)
pyautogui.PAUSE = 0

# function to open google snake game component in a new window
def open_game():
    webbrowser.open('https://g.co/kgs/KEtmYp', new=2)


# function to find the coordinates of the play button
def press_play():
    play_button = pyautogui.locateCenterOnScreen('play.png', confidence=0.7)
    pyautogui.click(play_button)
    time.sleep(1)
    pyautogui.press('space')
    time.sleep(1)
    pyautogui.press('right')


# function to find the coordinates of the food and return them as a tuple
def find_food(food_pic, top_left, bottom_right, width=17, height=15, confidence=0.75, grayscale=False):
    food = pyautogui.locateCenterOnScreen(food_pic,
                                          region=(top_left.x, top_left.y,
                                                  bottom_right.x - top_left.x, bottom_right.y - top_left.y),
                                          confidence=confidence
                                          )
    if food is None:
        return None
    # pyautogui.moveTo(food)
    # print('Raw Food Coord:', food)
    return (int((food.y - top_left.y) / ((bottom_right.y - top_left.y) / height)),
            int((food.x - top_left.x) / ((bottom_right.x - top_left.x) / width)))


# main function to run the game and use an algorithm to control the snake
def find_snake(head_pic, top_left, bottom_right, width=17, height=15, confidence=0.7, grayscale=False):
    snake_head = pyautogui.locateCenterOnScreen(head_pic,
                                                region=(top_left.x, top_left.y,
                                                        bottom_right.x - top_left.x,
                                                        bottom_right.y - top_left.y),
                                                confidence=confidence)
    if snake_head is None:
        return None
    pyautogui.moveTo(snake_head)
    snake_return = [(int((snake_head.y - top_left.y) / ((bottom_right.y - top_left.y) / height)),
                     int((snake_head.x - top_left.x) / ((bottom_right.x - top_left.x) / width)))]
    print(snake_return)
    return snake_return


def set_up():
    game_field = np.array([[0 for _ in range(17)] for _ in range(15)])
    start_time = time.time()
    top_left = pyautogui.locateCenterOnScreen('top_left.png', confidence=0.99)
    print('Top Left', top_left, time.time() - start_time)
    start_time = time.time()
    bottom_right = pyautogui.locateCenterOnScreen('bottom_right.png', confidence=0.95)

    print('Bottom Right', bottom_right, time.time() - start_time)
    if top_left is None or bottom_right is None:
        print('Top Left', top_left, 'Bottom Right', bottom_right)
        raise TypeError("Game field not found")
    starting_confidence = 0.90
    confidence = starting_confidence
    start_time = time.time()
    last_food = Point(-1, -1)
    time_of_death = time.time() + 20
    last_snake = [(-1, -1)]

    apple_center = Image.open('apple center.png')
    snake_head = Image.open('snake_head.png')
    apple_center.load()
    snake_head.load()

    while True:

        food = find_food(apple_center, top_left, bottom_right, confidence=confidence)
        if food is not None:
            confidence = starting_confidence
            if food[0] != last_food.x and food[1] != last_food.y:
                game_field[last_food.x][last_food.y] = 0
                last_food = Point(food[0], food[1])
                print("Food: ", food)
                game_field[food[0]][food[1]] = 5
                print('Time to find food: ', time.time() - start_time)
            start_time = time.time()
        else:
            confidence -= 0.05
        snake = find_snake(snake_head, top_left, bottom_right)
        if snake is not None and snake[0] != last_snake[0]:
            for x, y in last_snake:
                game_field[x][y] = 0
            game_field[snake[0][0]][snake[0][1]] = 2
            last_snake = snake
            for segment in snake[1:]:
                game_field[segment[0]][segment[1]] = 1
        # pyautogui.press(algorithm(game_field))
        if time.time() >= time_of_death:
            break


# algorithm to control the snake
def algorithm(game_field):
    directions = ['up', 'down', 'left', 'right']
    food = np.where(game_field == 5)
    snake_head = np.where(game_field == 2)

    snake_body = np.where(game_field == 1)
    if np.size(snake_head) == 0:
        return 'right'

    if snake_head[0] in [0, 1]:
        directions.remove('left')
    if snake_head[0] in [game_field.shape[0] - 1, game_field.shape[0] - 2]:
        directions.remove('right')
    if snake_head[1] in [0, 1]:
        directions.remove('up')
    if snake_head[1] in [game_field.shape[1] - 1, game_field.shape[1] - 2]:
        directions.remove('down')

    # return random direction
    return directions[np.random.randint(0, len(directions))]


if __name__ == '__main__':
    start = time.time()
    open_game()
    print('Opening game took', time.time() - start, 'seconds')
    time.sleep(4)
    start = time.time()
    press_play()
    print('Pressing play took', time.time() - start, 'seconds')
    set_up()
