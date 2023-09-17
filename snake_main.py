#################################################################
# FILE : snake_main.py
# WRITER : {israel_nankencki , israelnan , 305702334} , {ruslan levin, Rus234, 323383034}
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION: A program for snake game operation.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none, apart from our selves.
# WEB PAGES I USED: none
# NOTES:
#################################################################


import game_parameters
from game_display import GameDisplay
from typing import*


COOR_LIST = List[Tuple[int, int]]
APPLE_DATA = Tuple[int, int, int]
BOMB_DATA = Tuple[int, int, int, int]


def main_loop(gd: GameDisplay) -> None:
    """
    this function is the main operation of the game snake
    :param gd: GameDisplay object for executing game commands.
    :return: None
    """
    x, y = 10, 10
    snake_coordinates = [(x, y), (x, y-1), (x, y-2)]
    score = 0
    gd.show_score(score)
    time_count = 0
    current_radius = 0
    m, n, ra, time = bomb_data()
    lst = []
    apple1 = game_parameters.get_random_apple_data()
    apple2 = game_parameters.get_random_apple_data()
    apple3 = game_parameters.get_random_apple_data()
    apples = [apple1, apple2, apple3]
    len_to_append = 0
    draw_black(gd, snake_coordinates)
    gd.draw_cell(m, n, "red")
    lst.append(1)
    lst.append(2)
    while True:
        # command for longing the snake with one place at each round.
        if len_to_append > 0:
            long_snake(snake_coordinates)
            len_to_append -= 1
        # checks if the snake is eating the apple. if so, changing the apple and adding length to add the snake.
        for j in range(3):
            if ((apples[j][0], apples[j][1]) == (snake_coordinates[0][0] + 1, snake_coordinates[0][1])
                and check_direction(snake_coordinates) == 'Right') or \
                    ((apples[j][0], apples[j][1]) == (snake_coordinates[0][0] - 1, snake_coordinates[0][1])
                     and check_direction(snake_coordinates) == 'Left') or \
                    ((apples[j][0], apples[j][1]) == (snake_coordinates[0][0], snake_coordinates[0][1] - 1)
                     and check_direction(snake_coordinates) == 'Down') or \
                    ((apples[j][0], apples[j][1]) == (snake_coordinates[0][0], snake_coordinates[0][1] + 1)
                     and check_direction(snake_coordinates) == 'Up'):
                score += apples[j][2]
                gd.show_score(score)
                apples[j] = game_parameters.get_random_apple_data()
                len_to_append += 3
        # checks if any apple has generated on the bomb or on the snake buddy.
        check_apples(snake_coordinates, apples, (m, n))
        # prints all the current apples to the board.
        for i in apples:
            gd.draw_cell(i[0], i[1], "green")
            lst.append(1)
        # checks if the snake outside of the borders, shorts it and ends the game if so.
        if snake_head_outside_of_borders(snake_coordinates[0][0], snake_coordinates[0][1]):
            snake_coordinates.pop()
            draw_black(gd, snake_coordinates)
            gd.draw_cell(m, n, 'red')
            gd.end_round()
            break
        # operates the starting mode of the game.
        if len(lst) >= 6:
            key_clicked = gd.get_key_clicked()
            check_direction_and_move(snake_coordinates, key_clicked)
            draw_black(gd, snake_coordinates)
        # checks if the snake collided with itself or the bomb. if so, ends the game.
        if snake_collided(gd, snake_coordinates, (m, n)):
            gd.end_round()
            return
        # generating new bomb if it got it on one of the snake parts.
        elif (m, n) in snake_coordinates:
            m, n, ra, time = bomb_data()
        # prints the bomb while it suppose to.
        if time_count < time and len(lst) >= 6:
            gd.draw_cell(m, n, "red")
        # starts the explosion sequence when timer is done.
        elif time_count >= time:
            if current_radius <= ra:
                check = start_explosion(gd, m, n, current_radius, time_count)
                # checks if the snake had caught within the explosion. ends the game if so.
                for i in snake_coordinates:
                    if i in check:
                        gd.end_round()
                        return
                # checks if an apple had caught within the explosion. replace it if so.
                for i in apples:
                    if (i[0], i[1]) in check:
                        replace_apple(i, apples)
                current_radius += 1
            elif current_radius > ra:
                m, n, ra, time = bomb_data()
                time_count = 0
                current_radius = 0
        time_count += 1
        gd.end_round()


def bomb_data() -> BOMB_DATA:
    """
    this function generating bombs from its generator.
    :return: tuple with its coordinates, timer and explosion radius.
    """
    return game_parameters.get_random_bomb_data()


def long_snake(snake_coordinates: COOR_LIST) -> None:
    """
    this function checks if it's okay to add the snake from its tail and sends it to longing function.
    :param snake_coordinates: list of all snake coordinates.
    :return: None
    """
    if snake_coordinates[-1][0] == game_parameters.WIDTH - 1 or snake_coordinates[-1][1] == \
            game_parameters.HEIGHT - 1 or snake_coordinates[-1][0] == 0 or snake_coordinates[-1][1] == 0:
        long_snake_helper(snake_coordinates, snake_coordinates[0], snake_coordinates[1])
    else:
        long_snake_helper(snake_coordinates, snake_coordinates[-1], snake_coordinates[-2])


def long_snake_helper(snake_coordinates: COOR_LIST, i: Tuple[int, int], j: Tuple[int, int]) -> None:
    """
    this function check the tail/head direction and adds one part.
    :param snake_coordinates: list of all snake coordinates.
    :param i: snake tail/head coordinates.
    :param j: one part before tail/head of the snake, for direction reference.
    :return: None.
    """
    if i[0] == j[0] and j[1] > i[1]:
        snake_coordinates.append((i[0], i[1] - 1))
    elif i[0] == j[0] and j[1] < i[1]:
        snake_coordinates.append((i[0], i[1] + 1))
    elif i[1] == j[1] and j[0] > i[1]:
        snake_coordinates.append((i[0] - 1, i[1]))
    elif i[1] == j[1] and j[0] < i[0]:
        snake_coordinates.append((i[0] + 1, i[1]))


def start_explosion(gd: GameDisplay, m: int, n: int, radius: int, time=0) -> COOR_LIST:
    """
    this function starts the explosion sequence by sending the bomb data to its helper to execute.
    :param gd: GameDisplay object, for printing in orange.
    :param m: horizontal coordinate of the bomb.
    :param n: vertical coordinate of the bomb.
    :param radius: explosion radius of the bomb.
    :param time: timer for the bomb (unused).
    :return: list of coordinates of current explosion.
    """
    return helper_explosion(gd, m, n, radius, time, 0, [])


def helper_explosion(gd: GameDisplay, m: int, n: int, radius: int, time: int, radius_count: int,
                     lst: Optional[COOR_LIST]) -> COOR_LIST:
    """
    this function execute the explosion an
    :param gd: GameDisplay object, for printing in orange.
    :param m: horizontal coordinate of the bomb.
    :param n: vertical coordinate of the bomb.
    :param radius: explosion radius of the bomb.
    :param time: timer for the bomb (unused).
    :param radius_count: initial radius, for returning all coordinates within.
    :param lst: list of all current explosion coordinates.
    :return: list of all current explosion coordinates.
    """
    if radius_count > radius:
        return lst
    else:
        for i in range(game_parameters.WIDTH):
            for j in range(game_parameters.HEIGHT):
                if abs(m - i) + abs(n - j) == radius_count:
                    if 0 <= i < game_parameters.WIDTH and 0 <= j < game_parameters.HEIGHT:
                        lst.append((i, j))
                        if abs(m - i) + abs(n-j) == radius:
                            gd.draw_cell(i, j, "orange")
        return helper_explosion(gd, m, n, radius, time-1, radius_count+1, lst)


def check_direction(snake_coordinates: COOR_LIST) -> str:
    """
    this function checks the current direction of the snake for automatic progress.
    :param snake_coordinates: list of all snake coordinates.
    :return: string similar to key clicked.
    """
    if snake_coordinates[0][0] == snake_coordinates[1][0] and snake_coordinates[0][1] > snake_coordinates[1][1]:
        return 'Up'
    elif snake_coordinates[0][0] == snake_coordinates[1][0] and snake_coordinates[0][1] < snake_coordinates[1][1]:
        return 'Down'
    elif snake_coordinates[0][0] < snake_coordinates[1][0] and snake_coordinates[0][1] == snake_coordinates[1][1]:
        return 'Left'
    elif snake_coordinates[0][0] > snake_coordinates[1][0] and snake_coordinates[0][1] == snake_coordinates[1][1]:
        return 'Right'


def snake_head_outside_of_borders(i: int, j: int) -> bool:
    """
    this function checks whether the snake ren outside of the board.
    :param i: horizontal coordinate of the snake head.
    :param j: vertical coordinate of the snake head.
    :return: True if so.
    """
    if i == 0 or j == 0 or i == game_parameters.WIDTH - 1 or j == game_parameters.HEIGHT - 1:
        return True


def check_direction_and_move(snake_coordinates: COOR_LIST, key_clicked: Optional[str]) -> None:
    """
    this function checks in which direction the snake should move, and sends it to proper moving function.
    :param snake_coordinates: list of all snake coordinates.
    :param key_clicked: string of key clicked.
    :return: None.
    """
    if (key_clicked == 'Left' and check_direction(snake_coordinates) != "Right") \
            or (key_clicked is None and check_direction(snake_coordinates) == 'Left') \
            or (key_clicked == 'Right' and check_direction(snake_coordinates) == 'Left'):
        move_left(snake_coordinates)
    elif (key_clicked == 'Right' and check_direction(snake_coordinates) != 'Left') \
            or (key_clicked is None and check_direction(snake_coordinates) == 'Right') \
            or (key_clicked == 'Left' and check_direction(snake_coordinates) == 'Right'):
        move_right(snake_coordinates)
    elif (key_clicked == 'Up' and check_direction(snake_coordinates) != 'Down') \
            or (key_clicked is None and check_direction(snake_coordinates) == 'Up') \
            or (key_clicked == 'Down' and check_direction(snake_coordinates) == 'Up'):
        move_up(snake_coordinates)
    elif (key_clicked == 'Down' and check_direction(snake_coordinates) != 'Up') \
            or (key_clicked is None and check_direction(snake_coordinates) == 'Down') \
            or (key_clicked == 'Up' and check_direction(snake_coordinates) == 'Down'):
        move_down(snake_coordinates)


def move_right(snake_coordinates: COOR_LIST) -> None:
    """
    this function executing right move for the snake.
    :param snake_coordinates: list of all snake coordinates.
    :return: None.
    """
    for i in range(len(snake_coordinates) - 1, 0, -1):
        snake_coordinates[i] = snake_coordinates[i - 1]
    snake_coordinates[0] = (snake_coordinates[0][0] + 1, snake_coordinates[0][1])


def move_left(snake_coordinates: COOR_LIST) -> None:
    """
    this function executing left move for the snake.
    :param snake_coordinates: list of all snake coordinates.
    :return: None.
    """
    for i in range(len(snake_coordinates) - 1, 0, -1):
        snake_coordinates[i] = snake_coordinates[i - 1]
    snake_coordinates[0] = (snake_coordinates[0][0] - 1, snake_coordinates[0][1])


def move_up(snake_coordinates: COOR_LIST) -> COOR_LIST:
    """
    this function executing up move for the snake.
    :param snake_coordinates: list of all snake coordinates.
    :return: None.
    """
    for i in range(len(snake_coordinates) - 1, 0, -1):
        snake_coordinates[i] = snake_coordinates[i - 1]
    snake_coordinates[0] = (snake_coordinates[0][0], snake_coordinates[0][1] + 1)
    return snake_coordinates


def move_down(snake_coordinates: COOR_LIST) -> None:
    """
    this function executing down move for the snake.
    :param snake_coordinates: list of all snake coordinates.
    :return: None.
    """
    for i in range(len(snake_coordinates) - 1, 0, -1):
        snake_coordinates[i] = snake_coordinates[i - 1]
    snake_coordinates[0] = (snake_coordinates[0][0], snake_coordinates[0][1] - 1)


def snake_collided(gd: GameDisplay, snake_coordinates: COOR_LIST, bomb_coordinates: Tuple[int, int]) -> bool:
    """
    this function checks if the snake collided with itself or with the bomb and prints it in red as required.
    :param gd: GameDisplay object, for printing the collision point in red.
    :param snake_coordinates: list of all snake coordinates.
    :param bomb_coordinates: tuple with the bomb coordinates.
    :return: True if the snake did collided.
    """
    if snake_coordinates.count(snake_coordinates[0]) > 1:
        gd.draw_cell(bomb_coordinates[0], bomb_coordinates[1], 'red')
        return True
    elif bomb_coordinates == snake_coordinates[0]:
        gd.draw_cell(snake_coordinates[0][0], snake_coordinates[0][1], 'red')
        return True


def check_apples(snake_coordinates: COOR_LIST, apples: List[APPLE_DATA], bomb_coordinates: Tuple[int, int]) -> None:
    """
    this function checks if one of the apples generated on the snake or the bomb. if so. sends to a replacing function.
    :param snake_coordinates: list of all snake coordinates.
    :param apples: list of all apples, its coordinates and scores.
    :param bomb_coordinates: tuple with the bomb coordinates.
    :return: None.
    """
    for i in apples:
        if apples.count(i) > 1:
            replace_apple(i, apples)
        elif (i[0], i[1]) in snake_coordinates or (i[0], i[1]) == bomb_coordinates:
            replace_apple(i, apples)


def replace_apple(apple: APPLE_DATA, apples: List[APPLE_DATA]) -> None:
    """
    this function replacing apple when it should be replaced.
    :param apple: tuple with specific apple coordinates and score
    :param apples: list of all apples.
    :return: None.
    """
    apples.remove(apple)
    apples.append(game_parameters.get_random_apple_data())


def draw_black(gd: GameDisplay, snake_coordinates: COOR_LIST) -> None:
    """
    this function painting all snake coordinates in black.
    :param gd: GameDisplay object, for painting in black.
    :param snake_coordinates: list of all snake coordinates.
    :return: None.
    """
    for i in snake_coordinates:
        gd.draw_cell(i[0], i[1], "black")
