from .piece import Piece


class King(Piece):
    def __init__(self, x, y, player):
        super().__init__(x=x, y=y, player=player)
        self.type = 5
        self.incheck = False
        self.checkmate = False
        self.set_image()

    def put_incheck(self):
        self.incheck = True
        self.set_image()

    def put_outof_check(self):
        self.incheck = False
        self.set_image()

    def set_image(self):
        color_num = 0 if self.player == "white" else 1
        if not self.incheck:
            self.image = f"img\\{color_num}0{self.type}.png"
        else:
            self.image = f"img\\{color_num}0{self.type}c.png"

    def get_threats(self, board):
        threats = []
        for i in range(board.rows):
            for j in range(board.columns):
                if (board.board[i][j] != 0) and (board.board[i][j].player != self.player):
                    threats.extend(
                        board.board[i][j].get_valid_moves(board))
        return threats

    def get_valid_moves(self, board):
        valid_moves = []
        moves = [(self.x, self.y-1), (self.x+1, self.y-1), (self.x+1, self.y+1  # up, up+left/right
                                                            ),
                 (self.x-1, self.y), (self.x+1, self.y  # left, right
                                      ),
                 (self.x, self.y+1), (self.x-1, self.y-1), (self.x-1, self.y+1)]  # down, down+left/right
        # Todo castle
        # caste_moves = [(self.x-2, self.y),(self.x+2,self.y)] # queenside, kingside

        for move in moves:
            if board.move_within_bounds(move):
                if not board.cell_is_piece(move):
                    valid_moves.append(move)
                if (board.cell_is_piece(move)) and board.board[move[0]][move[1]].player != self.player:
                    valid_moves.append(move)

        return valid_moves
