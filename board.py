from pieces.pawn import Pawn
from pieces.king import King
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.bishop import Bishop
from pieces.rook import Rook
from pieces.piece import Piece


class Board:
    def __init__(self):
        self.rows = 8
        self.columns = 8
        self.board = [[0 for c in range(self.rows)]
                      for r in range(self.columns)]
        self.turn = "white"  # white starts
        self.turn_count = 0
        self.populate_board()

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def get_selected_piece(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if isinstance(self.board[i][j], Piece):
                    # check if we have a piece selected atm
                    if self.board[i][j].is_selected():
                        temp = self.board[i][j]
                        return temp
        return None

    def populate_board(self):
        # black pieces
        self.board[0][0] = Rook(0, 0, "black")
        self.board[1][0] = Knight(1, 0, "black")
        self.board[2][0] = Bishop(2, 0, "black")
        self.board[3][0] = Queen(3, 0, "black")
        self.board[4][0] = King(4, 0, "black")
        self.board[5][0] = Bishop(5, 0, "black")
        self.board[6][0] = Knight(6, 0, "black")
        self.board[7][0] = Rook(7, 0, "black")
        for i in range(8):
            self.board[i][1] = Pawn(i, 1, "black")

        # white pieces
        for j in range(8):
            self.board[j][6] = Pawn(j, 6, "white")
        self.board[0][7] = Rook(0, 7, "white")
        self.board[1][7] = Knight(1, 7, "white")
        self.board[2][7] = Bishop(2, 7, "white")
        self.board[3][7] = Queen(3, 7, "white")
        self.board[4][7] = King(4, 7, "white")
        self.board[5][7] = Bishop(5, 7, "white")
        self.board[6][7] = Knight(6, 7, "white")
        self.board[7][7] = Rook(7, 7, "white")
