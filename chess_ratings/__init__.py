import csv
import statistics

import types2
import utils
from types2 import Player, Game
from utils import chess_score
from elo import Elo
from glicko import Glicko


class Rating:
    ELO_CATEGORIES = [999, 1199, 1399, 1599, 1799, 1999, 2199, 2399, 2499, 2699, 10000]
    GLICKO_CATEGORIES = [750 + 0.625 * rating for rating in ELO_CATEGORIES]

    def __init__(self):
        self.__players = dict()

    def proceed_games(self, file: str):
        with open(file, newline='') as f:
            elo_rating = Elo()
            glicko_rating = Glicko()
            data = list(csv.reader(f))
            if len(data[0]) < 5 or data[0][0] != "id" or data[0][1] != "result" or data[0][2] != "white" \
                    or data[0][3] != "black" or data[0][4] != "datetime":
                raise TypeError("Data in CSV-file must contain "
                                "'id,result: [white|black|draw],white,black,datetime: %Y-%m-%d %H:%M:%S'")
            for row in data[1:]:
                game = Game(row)
                if game.id is not None and game.white != game.black:
                    if game.white not in self.__players.keys():
                        self.__players[game.white] = Player(game.white)
                    if game.black not in self.__players.keys():
                        self.__players[game.black] = Player(game.black)
                    elo_rating.rate(self.__players[game.white], self.__players[game.black], game.winner)
                    glicko_rating.rate(self.__players[game.white], self.__players[game.black],
                                       chess_score(game.winner), game.timestamp)

    def mean_diff(self):
        diffs = []
        for player in self.__players.values():
            idx1 = 0
            idx2 = 0
            for i in range(len(Rating.ELO_CATEGORIES)):
                if player.elo_rating <= Rating.ELO_CATEGORIES[i]:
                    idx1 = i
                    break
            for i in range(len(Rating.GLICKO_CATEGORIES)):
                if player.elo_rating <= Rating.GLICKO_CATEGORIES[i]:
                    idx2 = i
                    break
            diffs.append(idx1 - idx2)
        return statistics.mean(diffs)


def compare_elo_glicko(filename):
    rating = Rating()
    rating.proceed_games(filename)
    diff = rating.mean_diff()
    if diff == 0:
        print(f"Elo and Glicko ratings are equal!")
    elif diff > 0:
        print(f"Elo rating is higher than Glicko rating for {diff} categories in average")
    elif diff < 0:
        print(f"Glicko rating is higher than Elo rating for {-diff} categories in average")
    print(f"Ratings are based on the results of games from {filename}")


if __name__ == "__main__":
    compare_elo_glicko("ChessFull.csv")
