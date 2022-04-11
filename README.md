# Chess Ratings

## Introduction

Chess ratings is a python package, with implemented Elo and Glicko ratings and their comparison

## Usage

```python
import datetime
import chess_ratings

chess_ratings.compare_elo_glicko(filename)

# or

white = chess_ratings.Player(white_name)
black = chess_ratings.Player(black_name)
winner = chess_ratings.types2.Winner(winner)
date_time = datetime.datetime.strptime(string, fmt).timestamp()

elo = chess_ratings.Elo()
elo.rate(white, black, winner)

glicko = chess_ratings.Glicko()
glicko.rate(white, black, winner, date_time)
```