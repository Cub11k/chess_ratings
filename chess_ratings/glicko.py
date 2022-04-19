from math import log, sqrt, pi
from typing import Union

from types import Player, Winner
from utils import chess_score


class Glicko:
    Q = log(10) / 400
    C_2 = 34.6 * 34.6
    PERIOD = 315360
    NULL_RATING = 1500
    NULL_RD = 350

    def rate(self, white: Player, black: Player, scores: Union[Winner, tuple], date):
        if type(scores) is not tuple:
            scores = chess_score(scores)
        self.__update_old_rd(white, date)
        self.__update_old_rd(black, date)
        white.glicko_rating += Glicko.Q * self.__g(white) * (scores[0] - self.__e(white, black)) / (
                1 / white.glicko_rd ** 2 + 1 / self.__d_2(white, black))
        black.glicko_rating += Glicko.Q * self.__g(black) * (scores[1] - self.__e(black, white)) / (
                1 / black.glicko_rd ** 2 + 1 / self.__d_2(black, white))
        self.__update_rd(white, black)
        white.last_game = date
        black.last_game = date

    def __update_old_rd(self, player: Player, date):
        if player.last_game is None:
            return
        player.glicko_rd = min(350.0,
                               sqrt((player.glicko_rd ** 2) + Glicko.C_2 *
                                    ((date - player.last_game) / Glicko.PERIOD)))

    def __update_rd(self, player1: Player, player2):
        player1.glicko_rd = sqrt(1 / (1 / player1.glicko_rd ** 2 + 1 / self.__d_2(player1, player2)))
        player2.glicko_rd = sqrt(1 / (1 / player2.glicko_rd ** 2 + 1 / self.__d_2(player2, player1)))

    def __g(self, player: Player):
        return 1 / sqrt(1 + 3 * ((Glicko.Q * player.glicko_rd / pi) ** 2))

    def __e(self, player1: Player, player2: Player):
        return 1 / (1 + 10 ** (-self.__g(player2) * (player1.glicko_rating - player2.glicko_rating) / 400))

    def __d_2(self, player1: Player, player2: Player):
        e = self.__e(player1, player2)
        return 1 / (((Glicko.Q * self.__g(player2)) ** 2) * e * (1 - e))
