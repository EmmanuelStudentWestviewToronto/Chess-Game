from tkinter import Tk, Frame, Canvas, BOTH, TOP, Misc, Label
import time
import threading
from pieces.piece import Piece
from constants import WIDTH, HEIGHT, MARGIN, CELL_WIDTH, BACKGROUND_COLOR, WHITE, BLACK, SELECTED_COLOR


class ChessUI(Frame):
    def __init__(self, board):
        self.parent = Tk()
        self.board = board
        Frame.__init__(self, self.parent)

        self.t = threading.Thread(target=self.update_timer)
        self.initialize()

    def initialize(self):
        self.parent.title("Chess Game by RomJ55")
        self.pack(fill=BOTH)

        # UI Elements
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT,
                             background=BACKGROUND_COLOR)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.wtime_label = Label(self.canvas, text="Time: 00:00", font=(
            'comicsans', 20), background=BACKGROUND_COLOR)
        self.wtime_label.place(x=WIDTH-MARGIN*2-10, y=HEIGHT-MARGIN//2-20)

        self.btime_label = Label(self.canvas, text="Time: 00:00", font=(
            'comicsans', 20), background=BACKGROUND_COLOR)
        self.btime_label.place(x=WIDTH-MARGIN*2-10, y=MARGIN//2-20)

        self.draw_start_screen()

    def draw_start_screen(self):
        self.draw_grid()
        self.draw_squares()
        self.start_canvas = Canvas(
            self, width=WIDTH-100, height=HEIGHT//6, background="#444444")

        self.start_canvas.create_text(350, 60,
                                      text="Click here to start...", font="comicsans 36", fill="#ffffff")
        self.start_canvas.place(x=50, y=HEIGHT//2.5)
        Misc.lift(self.start_canvas)
        self.start_canvas.bind("<Button-1>", self.load_gameui)

    def load_gameui(self, event):
        self.board.run_game()
        self.start_canvas.destroy()
        time.sleep(0.3)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.clicked)
        self.t.start()

    def draw_board(self):
        if not self.board.is_winner:
            self.draw_grid()
            self.draw_squares()
            self.draw_pieces()
            self.draw_labels()
        else:
            self.canvas.unbind("<Button-1>")
            winner = "black" if self.board.white_time <= 0 else "white"
            self.draw_grid()
            self.draw_squares()
            self.end_canvas = Canvas(
                self, width=WIDTH-100, height=HEIGHT//6, background="#444444")

            self.end_canvas.create_text(350, 60,
                                        text=f"{winner} won!".upper(), font="comicsans 36", fill="#ffffff")
            self.end_canvas.place(x=50, y=HEIGHT//2.5)
            Misc.lift(self.end_canvas)

        self.update()

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
                if self.board.cell_is_piece((i, j)):
                    x, y = self.board.board[i][j].position
                    self.board.board[i][j].draw_self(
                        self.canvas, (MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH//2)
                    if self.board.board[i][j].is_selected():
                        self.canvas.create_oval((MARGIN+x*CELL_WIDTH)+5, (MARGIN+y*CELL_WIDTH)+5,
                                                (MARGIN+x*CELL_WIDTH)+CELL_WIDTH-5, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH-5, outline=SELECTED_COLOR, tag="select_oval")

    def draw_labels(self):
        self.canvas.delete("turn_text")
        # turn text
        self.canvas.create_text(WIDTH//2, HEIGHT-MARGIN//2,
                                text=f"{self.board.turn} Turn".upper(), tag="turn_text", font="comicsans 30")

    def draw_moves(self, moves):
        if len(moves) > 0:
            for move in moves:
                self.canvas.create_oval(MARGIN+move[0]*CELL_WIDTH+30, MARGIN+move[1]*CELL_WIDTH+30,
                                        MARGIN+move[0]*CELL_WIDTH+CELL_WIDTH-30, MARGIN+move[1]*CELL_WIDTH+CELL_WIDTH-30, fill=SELECTED_COLOR)

    def update_timer(self):
        if self.board.turn == "white":
            timer = self.format_time(self.board.white_time)
            self.wtime_label["text"] = timer
            self.board.white_time -= 1
        else:
            timer = self.format_time(self.board.black_time)
            self.btime_label["text"] = timer
            self.board.black_time -= 1

        self.after(1000, self.update_timer)

    def format_time(self, timer):
        if timer > 0:
            minutes = timer // 60
            seconds = timer % 60
            if seconds > 9:
                formatted_string = f"Time: {str(minutes)}:{str(seconds)}"
            else:
                formatted_string = f"Time: {str(minutes)}:0{str(seconds)}"
        else:
            formatted_string = "Times up!"
            self.board.is_winner = True
            self.board.stop_game()
            self.draw_board()
        return formatted_string

    def clicked(self, event):
        x, y, = event.x, event.y
        # if we clicked on the board
        if MARGIN < x < WIDTH-MARGIN and MARGIN < y < WIDTH-MARGIN:
            x_grid_position = int(x//CELL_WIDTH-1)
            y_grid_position = int(y//CELL_WIDTH-1)
            # if we clicked on a piece
            if self.board.cell_is_piece((x_grid_position, y_grid_position)):
                # check if turn and piece color match
                if self.board.board[x_grid_position][y_grid_position].player == self.board.turn:
                    # it the piece is selected, we unselect it
                    if self.board.board[x_grid_position][y_grid_position].is_selected():
                        self.board.board[x_grid_position][y_grid_position].unselect(
                        )
                    # if the piece is not selected...
                    else:
                        # ... we unselect every other piece
                        self.board.unselect_all()
                        self.canvas.delete("select-oval")
                        # and select the new one
                        self.board.board[x_grid_position][y_grid_position].select(
                        )
                        moves = self.board.board[x_grid_position][y_grid_position].get_valid_moves(
                            self.board)

                    self.draw_board()
                    try:
                        self.draw_moves(moves)
                    except UnboundLocalError:
                        pass
                # if turn and color don't match
                else:
                    # check if we have a piece selected atm
                    temp = self.board.get_selected_piece()
                    if temp is not None:
                        valid = temp.get_valid_moves(self.board)
                        if (x_grid_position, y_grid_position) in valid:
                            self.board.handle_piece_move(
                                temp, (x_grid_position, y_grid_position))
                            try:
                                self.t.start()
                            except RuntimeError:
                                pass
                            self.draw_board()
            # if we clicked on a free cell
            else:
                temp = self.board.get_selected_piece()
                if temp is not None:
                    valid = temp.get_valid_moves(self.board)
                    if (x_grid_position, y_grid_position) in valid:
                        self.board.handle_piece_move(
                            temp, (x_grid_position, y_grid_position))
                        try:
                            self.t.start()
                        except RuntimeError:
                            pass
                        self.draw_board()
