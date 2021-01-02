from ui import ChessUI
from board import Board

board = Board(900)  # time in seconds 900/60 = 15 Minutes
ui = ChessUI(board)

ui.mainloop()
