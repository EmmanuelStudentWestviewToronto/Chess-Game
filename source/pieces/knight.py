from tkinter import PhotoImage
from .piece import Piece


class Knight(Piece):
    def __init__(self, x, y, player):
        super().__init__(x=x, y=y, player=player)
        self.type = 1
        self.set_image()

    def set_image(self):
        color_num = 0 if self.player == "white" else 1
        self.image = f"img\\{color_num}0{self.type}.png"

    def get_valid_moves(self, board):
        valid_moves = []
        moves = [(self.x-1, self.y-2), (self.x+1, self.y-2),  # up and left/right
                 (self.x-1, self.y+2), (self.x+1, self.y+2),  # down and left/right
                 (self.x+2, self.y-1), (self.x+2, self.y+1),  # right and up/down
                 (self.x-2, self.y-1), (self.x-2, self.y + 1)]  # left and up/down

        for move in moves:
            if board.move_within_bounds(move):
                if not board.cell_is_piece(move):
                    valid_moves.append(move)
                if (board.cell_is_piece(move)) and board.board[move[0]][move[1]].player != board.turn:
                    valid_moves.append(move)

        return valid_moves
