import datetime
import chess_ratings

chess_ratings.compare_elo_glicko("ChessFull.csv")

# or

white = chess_ratings.Player("white_name")
black = chess_ratings.Player("black_name")
winner = chess_ratings.types2.Winner("white")
date_time = datetime.datetime.strptime("2021-10-31 13:34:23", "%Y-%m-%d %H:%M:%S").timestamp()

elo = chess_ratings.Elo()
elo.rate(white, black, winner)

glicko = chess_ratings.Glicko()
glicko.rate(white, black, winner, date_time)

print(f"White player: name={white.name} elo={white.elo_rating} glicko={white.glicko_rating}")
print(f"Black player: name={black.name} elo={black.elo_rating} glicko={black.glicko_rating}")
