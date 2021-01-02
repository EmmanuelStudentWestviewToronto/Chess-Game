from tkinter import Tk, Frame, Canvas, BOTH, TOP, Misc, Label, Button, FIRST
import time
import threading
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

        self.wtime_label = Label(self.canvas, text=f"Time: {self.board.white_time//60}:00", font=(
            'comicsans', 20), background=BACKGROUND_COLOR)
        self.wtime_label.place(x=WIDTH-MARGIN*2-10, y=HEIGHT-MARGIN//2-20)

        self.btime_label = Label(self.canvas, text=f"Time: {self.board.black_time//60}:00", font=(
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
            self.draw_misc()
        else:
            self.draw_grid()
            self.draw_squares()
            self.draw_pieces()
            end_canvas = Canvas(
                self, width=WIDTH-100, height=HEIGHT//6-20, background="#444444")

            end_canvas.create_text(350, 60,
                                   text=f"Winner: {self.board.winner} !".upper(), font="comicsans 36", fill="#ffffff")
            end_canvas.place(x=50, y=HEIGHT//2.5)
            Misc.lift(end_canvas)

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
                x_start_h, y_start_h, x_end_h, y_end_h, fill="BLACK", width=3)
            # vertical lines
            self.canvas.create_line(
                x_start, y_start, x_end, y_end, fill="BLACK", width=3)

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
        self.canvas.delete("marked-arrow")
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                if self.board.cell_is_piece((i, j)):
                    x, y = self.board.board[i][j].position
                    self.board.board[i][j].draw_self(
                        self.canvas, (MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH//2)
                    if self.board.board[i][j].is_selected():
                        self.canvas.create_oval((MARGIN+x*CELL_WIDTH)+5, (MARGIN+y*CELL_WIDTH)+5,
                                                (MARGIN+x*CELL_WIDTH)+CELL_WIDTH-5, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH-5, outline=SELECTED_COLOR, tag="select_oval")
                    if self.board.board[i][j].type == 5 and self.board.board[i][j].marked:
                        self.canvas.create_line((MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2-1, (MARGIN+y*CELL_WIDTH)+10, (
                            MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2-1, (MARGIN+y*CELL_WIDTH)-15, fill="#ff0000", arrow=FIRST, width=5, tag="marked-arrow")

    def draw_misc(self):
        self.canvas.delete("turn_text")
        # turn text
        self.canvas.create_text(WIDTH//2, HEIGHT-MARGIN//2,
                                text=f"{self.board.turn} Turn".upper(), tag="turn_text", font="comicsans 30")

        self.giveup_button = Button(
            self.canvas, text="Give up", font="comicsans 20", fg="#ff0000", command=self.end_game, borderwidth=8)
        self.giveup_button.place(x=80, y=HEIGHT-70)

    def draw_moves(self, moves):
        if len(moves) > 0:
            for move in moves:
                self.canvas.create_oval(MARGIN+move[0]*CELL_WIDTH+30, MARGIN+move[1]*CELL_WIDTH+30,
                                        MARGIN+move[0]*CELL_WIDTH+CELL_WIDTH-30, MARGIN+move[1]*CELL_WIDTH+CELL_WIDTH-30, fill=SELECTED_COLOR)

    def end_game(self):
        self.board.stop_game("black" if self.board.turn ==
                             "white" else "white")
        self.canvas.delete("turn_text")
        self.canvas.unbind("<Button-1>")
        self.giveup_button.destroy()
        self.draw_board()

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
            self.end_game()
        return formatted_string

    def initiate_piece_move(self, x, y):
        piece = self.board.get_selected_piece()
        if piece is not None:
            if not piece.type == 5:  # if it's not a king
                valid_moves = piece.get_valid_moves(self.board)
                if (x, y) in valid_moves:
                    self.board.handle_piece_move(
                        piece, (x, y))
            else:
                valid_kingmoves, valid_castle_moves = piece.get_valid_moves(
                    self.board)
                if (x, y) in valid_kingmoves:
                    self.board.handle_piece_move(
                        piece, (x, y))
                elif len(valid_castle_moves) > 0 and ((x, y) == valid_castle_moves[0][1] or (x, y) == valid_castle_moves[1][1]):
                    if (x, y) == valid_castle_moves[0][1]:
                        self.board.handle_castle_move(
                            piece, valid_castle_moves[0])
                    else:
                        self.board.handle_castle_move(
                            piece, valid_castle_moves[1])
            try:
                self.t.start()
            except RuntimeError:
                pass
            self.draw_board()
        # do nothing if no piece is selected

    def clicked(self, event):
        x, y, = event.x, event.y
        if MARGIN < x < WIDTH-MARGIN and MARGIN < y < WIDTH-MARGIN:  # if we clicked on the game-board
            x_grid_pos = int(x//CELL_WIDTH-1)
            y_grid_pos = int(y//CELL_WIDTH-1)
            # if we clicked on a piece
            if self.board.cell_is_piece((x_grid_pos, y_grid_pos)):
                # if turn and piece color match
                if self.board.board[x_grid_pos][y_grid_pos].player == self.board.turn:
                    # it the piece is selected...
                    if self.board.board[x_grid_pos][y_grid_pos].is_selected():
                        self.board.board[x_grid_pos][y_grid_pos].unselect(
                        )  # ...we unselect it
                    # if the piece is not selected...
                    else:
                        # ... we unselect every other piece
                        self.board.unselect_all()
                        self.canvas.delete("select-oval")
                        self.board.board[x_grid_pos][y_grid_pos].select(
                        )  # and select the new one
                        # moves = self.board.board[x_grid_pos][y_grid_pos].get_valid_moves(
                        #     self.board)
                    self.draw_board()
                    # try:
                    #     self.draw_moves(moves)
                    # except UnboundLocalError:
                    #     pass
                # if turn and color don't match
                else:
                    self.initiate_piece_move(x_grid_pos, y_grid_pos)
            # not a piece
            else:
                self.initiate_piece_move(x_grid_pos, y_grid_pos)
