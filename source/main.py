from ui import ChessUI
from board import Board

board = Board(900)  # time in seconds
ui = ChessUI(board)

ui.mainloop()
