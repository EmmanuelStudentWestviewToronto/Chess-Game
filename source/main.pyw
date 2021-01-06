from ui import ChessUI
from game import Game

game = Game()  # time in seconds default=900. 900/60 = 15 Minutes
ui = ChessUI(game)

ui.mainloop()
