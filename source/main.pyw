from ui import ChessUI
from board import Board

board = Board()  # time in seconds default=900. 900/60 = 15 Minutes
ui = ChessUI(board)

ui.mainloop()
