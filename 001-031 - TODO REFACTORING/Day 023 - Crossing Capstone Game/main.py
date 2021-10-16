# import logging
import random
import time
from turtle import Screen

import numba

from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
from matplotlib.path import Path


class Game:

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    REFRESH_TIME = 0.1
    WAITING_TIME = 3

    def __init__(self):
        self.screen = Screen()
        self.screen.clear()
        self.screen.setup(width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT)
        self.screen.tracer(False)
        self.player = Player()
        self.score_board = Scoreboard()
        self.car_manager = CarManager(self.screen)
        self.game_is_on = True
        self.screen.listen()

    @numba.jit(forceobj=True)
    def is_collision(self) -> bool:
        player_map: Path = self.player.get_shape_polygon()
        # start_time = time.time()
        for car in self.car_manager.cars:
            car_map: Path = car.get_get_shape_polygon()
            if player_map.intersects_path(car_map) or \
                player_map.contains_point(car_map.vertices.tolist()[0]) or \
                    car_map.contains_point(player_map.vertices.tolist()[0]):
                # logging.warning(f"{player_map}, {car_map}")
                return True
        # logging.warning("Time:" + str(time.time() - start_time))
        return False

    def play_game(self):
        while self.game_is_on:
            time.sleep(self.REFRESH_TIME)
            if random.SystemRandom().randint(1, 6) == 1:
                self.car_manager.generate_car()
            self.car_manager.move_increment = self.car_manager.STARTING_MOVE_DISTANCE + \
                self.car_manager.MOVE_INCREMENT * (self.player.level - self.player.LEVEL)
            self.car_manager.move_cars()
            self.score_board.level = self.player.level
            self.score_board.print_level()
            self.screen.update()
            if self.is_collision():
                self.score_board.print_game_over()
                self.game_is_on = False


while True:
    Game().play_game()
    time.sleep(Game.WAITING_TIME)
