from .piece import Piece
from tkinter import PhotoImage


class Pawn(Piece):
    def __init__(self, x, y, player):
        super().__init__(x=x, y=y, player=player)
        self.type = 0
        self.set_image()

    def set_image(self):
        color_num = 0 if self.player == "white" else 1
        self.image = f"img\\{color_num}0{self.type}.png"

    def get_valid_moves(self, board):
        valid_moves = []
        moves_w = [(self.x, self.y-1), (self.x, self.y-2),
                   (self.x-1, self.y-1), (self.x + 1, self.y - 1)]
        moves_b = [(self.x, self.y+1), (self.x, self.y+2),
                   (self.x-1, self.y+1), (self.x + 1, self.y + 1)]

        if self.player == "white":
            if (-1 < moves_w[0][0] < 8) and (-1 < moves_w[0][1] < 8):
                if not isinstance(board.board[moves_w[0][0]][moves_w[0][1]], Piece):
                    valid_moves.append(moves_w[0])
            if (-1 < moves_w[1][0] < 8) and (-1 < moves_w[1][1] < 8):
                if (not isinstance(board.board[moves_w[1][0]][moves_w[1][1]], Piece)
                    ) and not isinstance(board.board[self.x][self.y-1], Piece) and self.y == 6:
                    valid_moves.append(moves_w[1])
            for i in range(2, len(moves_w)):
                if (-1 < moves_w[i][0] < 8) and (-1 < moves_w[i][1] < 8):
                    if (isinstance(board.board[moves_w[i][0]][moves_w[i][1]], Piece
                                   ) and board.board[moves_w[i][0]][moves_w[i][1]].player != board.turn):
                        valid_moves.append(moves_w[i])
        else:
            if (-1 < moves_b[0][0] < 8) and (-1 < moves_b[0][1] < 8):
                if not isinstance(board.board[moves_b[0][0]][moves_b[0][1]], Piece):
                    valid_moves.append(moves_b[0])
            if (-1 < moves_b[1][0] < 8) and (-1 < moves_b[1][1] < 8):
                if (not isinstance(board.board[moves_b[1][0]][moves_b[1][1]], Piece)
                    ) and not isinstance(board.board[self.x][self.y+1], Piece) and self.y == 1:
                    valid_moves.append(moves_b[1])
            for i in range(2, len(moves_b)):
                if (-1 < moves_b[i][0] < 8) and (-1 < moves_b[i][1] < 8):
                    if (isinstance(board.board[moves_b[i][0]][moves_b[i][1]], Piece
                                   ) and board.board[moves_b[i][0]][moves_b[i][1]].player != board.turn):
                        valid_moves.append(moves_b[i])

        return valid_moves

    def draw_path(self, start, end):
        x_start, y_start = start
        x_end, y_end = end

    def draw_self(self, canvas, x, y):
        img = PhotoImage(file=self.image)
        canvas.create_image(x, y, image=img)
        self.image_garbo = img
