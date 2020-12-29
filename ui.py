from pieces.piece import Piece
from board import Board
from constants import WIDTH, HEIGHT, MARGIN, CELL_WIDTH, BACKGROUND_COLOR, WHITE, BLACK
from tkinter import *


class ChessUI(Frame):
    def __init__(self, board):
        self.parent = Tk()
        self.board = board
        Frame.__init__(self, self.parent)

        self.initialize()

    def initialize(self):
        self.parent.title("Chess Game by RomJ55")
        self.pack(fill=BOTH)

        # UI Elements
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT,
                             background=BACKGROUND_COLOR)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.draw_board()
        # self.draw_pieces()

    def draw_board(self):
        self.draw_grid()
        self.draw_squares()

    def draw_grid(self):
        for i in range(self.board.rows+1):
            x_start = MARGIN + i*CELL_WIDTH
            y_start = MARGIN
            x_end = MARGIN + i * CELL_WIDTH
            y_end = HEIGHT-MARGIN

            x_start_h = MARGIN
            y_start_h = MARGIN + i*CELL_WIDTH
            x_end_h = WIDTH-MARGIN
            y_end_h = MARGIN + i*CELL_WIDTH
            # horizontal lines
            self.canvas.create_line(
                x_start_h, y_start_h, x_end_h, y_end_h, fill="BLACK", width=2)
            # vertical lines
            self.canvas.create_line(
                x_start, y_start, x_end, y_end, fill="BLACK", width=2)

    def draw_squares(self):
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                x_start = MARGIN + i*CELL_WIDTH
                y_start = MARGIN + j*CELL_WIDTH
                x_end = MARGIN + i * CELL_WIDTH + CELL_WIDTH
                y_end = MARGIN + j * CELL_WIDTH + CELL_WIDTH
                fill_color = BLACK if (j+i) % 2 else WHITE
                self.canvas.create_rectangle(
                    x_start, y_start, x_end, y_end, fill=fill_color)
                if isinstance(self.board.board[i][j], Piece):
                    x, y = self.board.board[i][j].position
                    self.board.board[i][j].draw_self(
                        self.canvas, (MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH//2)
