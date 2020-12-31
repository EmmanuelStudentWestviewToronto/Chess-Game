from .piece import Piece


class King(Piece):
    def __init__(self, x, y, player):
        super().__init__(x=x, y=y, player=player)
        self.type = 5
        self.is_check = False
        self.is_checkmate = False
        self.set_image()

    def set_image(self):
        color_num = 0 if self.player == "white" else 1
        self.image = f"img\\{color_num}0{self.type}.png"

    def get_valid_moves(self, board):
        valid_moves = []
        moves = [(self.x, self.y-1), (self.x+1, self.y-1), (self.x+1, self.y+1  # up, up+left/right
                                                            ),
                 (self.x-1, self.y), (self.x+1, self.y  # left, right
                                      ),
                 (self.x, self.y+1), (self.x-1, self.y-1), (self.x-1, self.y+1)]  # down, down+left/right
        # Todo castle

        for move in moves:
            if board.move_within_bounds(move):
                # todo something with self.is_check & self.is_checkmate
                if not board.cell_is_piece(move):
                    valid_moves.append(move)
                if (board.cell_is_piece(move)) and board.board[move[0]][move[1]].player != board.turn:
                    valid_moves.append(move)

        return valid_moves
