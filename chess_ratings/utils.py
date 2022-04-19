from types import Winner


def chess_score(winner: Winner):
    if winner.id == Winner.DRAW:
        return 0.5, 0.5
    if winner.id == Winner.WHITE:
        return 1.0, 0.0
    if winner.id == Winner.BLACK:
        return 0.0, 1.0
