from pieces import rook


class Board:
    def __init__(self):
        self.rows = 8
        self.columns = 8
        self.board = [[rook.Rook(r, c, "black") for r in range(self.rows)]
                      for c in range(self.columns)]
        self.turn = "white"  # white starts

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
