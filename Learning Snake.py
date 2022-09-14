# Code to play the google snake game via an algorithm
import time
# imports
import webbrowser
import numpy as np
import cv2
import pyautogui
from pyautogui import Point

print(cv2.__version__)


# function to open google snake game component in a new window
def open_game():
    webbrowser.open('https://g.co/kgs/KEtmYp', new=2)


# function to find the coordinates of the play button
def press_play():
    play_button = pyautogui.locateCenterOnScreen('play.png', confidence=0.9)
    pyautogui.click(play_button)
    time.sleep(1)
    pyautogui.press('space')
    time.sleep(1)
    pyautogui.press('right')


# function to find the coordinates of the food and return them as a tuple
def find_food(top_left, bottom_right, width=17, height=15, confidence=0.75):
    food = pyautogui.locateCenterOnScreen('apple center.png',
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
    while True:
        food = find_food(top_left, bottom_right, confidence=confidence)
        if food is not None:
            confidence = starting_confidence
            if food[0] != last_food.x and food[1] != last_food.y:
                game_field[last_food.x][last_food.y] = 0
                last_food = Point(food[0], food[1])
                print("Food: ", food)
                game_field[food[0]][food[1]] = 5
                print('------------TOP------------')
                for field in game_field:
                    print(field)
                print('------------BOTTOM------------')
                print('Time to find food: ', time.time() - start_time)
                print('Food confidence: ', confidence)
            time.sleep(0.001)
            start_time = time.time()
        else:
            confidence -= 0.05


# algorithm to control the snake
def algorithm(game_field):
    direction = 'right'
    return direction


if __name__ == '__main__':
    start = time.time()
    open_game()
    print('Opening game took', time.time() - start, 'seconds')
    time.sleep(4)
    start = time.time()
    press_play()
    print('Pressing play took', time.time() - start, 'seconds')
    time.sleep(0.1)
    set_up()
