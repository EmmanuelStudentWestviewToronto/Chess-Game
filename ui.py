from tkinter import *
from pieces.piece import Piece
from constants import WIDTH, HEIGHT, MARGIN, CELL_WIDTH, BACKGROUND_COLOR, WHITE, BLACK


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
        self.canvas.bind("<Button-1>", self.clicked)

        self.draw_board()

    def draw_board(self):
        self.draw_grid()
        self.draw_squares()
        self.draw_pieces()
        self.draw_labels()

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

    def draw_pieces(self):
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                if isinstance(self.board.board[i][j], Piece):
                    x, y = self.board.board[i][j].position
                    self.board.board[i][j].draw_self(
                        self.canvas, (MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH//2)
                    if self.board.board[i][j].is_selected():
                        self.canvas.create_oval((MARGIN+x*CELL_WIDTH)+5, (MARGIN+y*CELL_WIDTH)+5,
                                                (MARGIN+x*CELL_WIDTH)+CELL_WIDTH-5, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH-5, outline="#ff00ff", tag="select_oval")

    def draw_labels(self):
        # turn text
        self.canvas.create_text(WIDTH//2, HEIGHT-MARGIN//2,
                                text=f"{self.board.turn} Turn".upper(), tag="turn_text", font="comicsans 30")

        # timers
        self.canvas.create_text(WIDTH-MARGIN*2, MARGIN//2,
                                text=f"Time: 10:00", tag="black_timer", font="comicsans 20")
        self.canvas.create_text(WIDTH-MARGIN*2, HEIGHT-MARGIN//2,
                                text=f"Time: 10:00", tag="white_timer", font="comicsans 20")

    def clicked(self, event):
        x, y, = event.x, event.y
        if MARGIN < x < WIDTH-MARGIN and MARGIN < y < WIDTH-MARGIN:
            x_grid_position = int(x//CELL_WIDTH-1)
            y_grid_position = int(y//CELL_WIDTH-1)
            # if we clicked on a piece
            if isinstance(self.board.board[x_grid_position][y_grid_position], Piece):
                # check if turn and piece color match
                if self.board.board[x_grid_position][y_grid_position].player == self.board.turn:
                    # it the piece is selected, we unselect it
                    if self.board.board[x_grid_position][y_grid_position].is_selected():
                        self.board.board[x_grid_position][y_grid_position].unselect(
                        )
                    # if the piece is not selected...
                    else:
                        for i in range(self.board.rows):
                            for j in range(self.board.columns):
                                if isinstance(self.board.board[i][j], Piece):
                                    # ... we unselect every other friendly piece
                                    self.board.board[i][j].unselect()
                        self.canvas.delete("select-oval")
                        # and select the new one
                        self.board.board[x_grid_position][y_grid_position].select(
                        )
                    self.draw_board()
                    self.update()
                # if turn and color don't match
                else:
                    temp = self.board.get_selected_piece()
                    if temp is not None:
                        # todo : if temp.is_valid_move((x_grid_position, y_grid_position)):
                        self.board.board[temp.x][temp.y] = 0
                        temp.move((x_grid_position, y_grid_position))
                        self.board.board[x_grid_position][y_grid_position] = temp
                        self.draw_board()
                        self.update()
            # if we clicked on a free cell
            else:
                temp = self.board.get_selected_piece()
                if temp is not None:
                    # todo : if temp.is_valid_move((x_grid_position, y_grid_position)):
                    self.board.board[temp.x][temp.y] = 0
                    temp.move((x_grid_position, y_grid_position))
                    self.board.board[x_grid_position][y_grid_position] = temp
                    self.draw_board()
                    self.update()
