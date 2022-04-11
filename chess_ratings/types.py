import datetime


class Winner:
    DRAW = 0
    WHITE = 1
    BLACK = 2

    def __init__(self, winner: str):
        if winner == "draw":
            self.id = Winner.DRAW
        elif winner == "white":
            self.id = Winner.WHITE
        elif winner == "black":
            self.id = Winner.BLACK


class Player:
    ELO_NULL_RATING = 1000
    ELO_NULL_K_FACTOR = 40
    GLICKO_NULL_RATING = 1500
    GLICKO_NULL_RD = 350

    def __init__(self, name: str = None):
        self.name = name
        self.last_game = None
        self.elo_rating = Player.ELO_NULL_RATING
        self.elo_k_factor = Player.ELO_NULL_K_FACTOR
        self.glicko_rating = Player.GLICKO_NULL_RATING
        self.glicko_rd = Player.GLICKO_NULL_RD


class Game:
    def __init__(self, row: list[str] = None):
        if row is not None:
            if len(row) < 5:
                raise TypeError("Game must be initialized with a row of at least 5 values")
            self.id = row[0]
            self.white = row[2]
            self.black = row[3]
            self.winner = Winner(row[1])
            self.timestamp = datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S").timestamp()
        else:
            self.id = None
