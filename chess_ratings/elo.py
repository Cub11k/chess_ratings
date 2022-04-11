from types2 import Player, Winner
from utils import chess_score


class Elo:
    NULL_RATING = 1000
    PRO_RATING = 2400
    NULL_K_FACTOR = 40
    REGULAR_K_FACTOR = 20
    PRO_K_FACTOR = 10

    def rate(self, white: Player, black: Player, winner: Winner):
        expectation = self.__expectation(white.elo_rating, black.elo_rating)
        scores = chess_score(winner)

        white.elo_rating += int(white.elo_k_factor * (scores[0] - expectation[0]) // 1)
        if white.elo_rating < Elo.NULL_RATING:
            white.elo_rating = Elo.NULL_RATING
        self.__update_k_factor(white)

        black.elo_rating += int(black.elo_k_factor * (scores[1] - expectation[1]) // 1)
        if white.elo_rating < Elo.NULL_RATING:
            white.elo_rating = Elo.NULL_RATING
        self.__update_k_factor(black)

    def __expectation(self, rating1: int, rating2: int):
        return 1 / (1 + 10 ** ((rating2 - rating1) / 400)), 1 / (1 + 10 ** ((rating1 - rating2) / 400))

    def __update_k_factor(self, player):
        if player.elo_rating > Elo.NULL_RATING:
            if player.elo_rating >= Elo.PRO_RATING:
                player.elo_k_factor = Elo.PRO_K_FACTOR
            else:
                player.elo_k_factor = Elo.REGULAR_K_FACTOR
