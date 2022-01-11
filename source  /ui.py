from tkinter import Tk, Frame, Canvas, BOTH, TOP, Misc, Label, Button, FIRST, DISABLED, NORMAL
import time
import threading
from constants import WIDTH, HEIGHT, MARGIN, CELL_WIDTH, BACKGROUND_COLOR, WHITE, BLACK, SELECTED_COLOR, STARTEND_BACKGROUND


class ChessUI(Frame):
    def __init__(self, game):
        self.parent = Tk()
        self.game = game
        Frame.__init__(self, self.parent)

        self.thread = threading.Thread(target=self.update_timer)
        self.initialize()

    def initialize(self):
        self.parent.title("Chess Game by RomJ55")
        self.pack(fill=BOTH)

        # UI Elements
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT,
                             background=BACKGROUND_COLOR)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.wtime_label = Label(self.canvas, text=f"Time: {self.game.timer_save//60}:00", font=(
            'comicsans', 20), background=BACKGROUND_COLOR)
        self.btime_label = Label(self.canvas, text=f"Time: {self.game.timer_save//60}:00", font=(
            'comicsans', 20), background=BACKGROUND_COLOR)
        self.wtime_label.place(x=WIDTH-MARGIN*2-65, y=HEIGHT-MARGIN//2-30)
        self.btime_label.place(x=WIDTH-MARGIN*2-65, y=MARGIN//2-5)
        self.giveup_button = Button(
            self.canvas, text="Give up", font="comicsans 20", fg="#ff0000", command=self.end_game_handler, borderwidth=2)
        self.giveup_button.place(x=80, y=HEIGHT-70)
        self.giveup_button["state"] = DISABLED

        self.draw_start_screen()

    def draw_start_screen(self):
        self.draw_grid()
        self.draw_squares()
        start_canvas = Canvas(
            self, width=WIDTH-100, height=HEIGHT//4-20, background=STARTEND_BACKGROUND)
        start_canvas.create_text(WIDTH//2-50, 35,
                                 text="Welcome to Chess!", font="comicsans 36", fill=WHITE)
        start_canvas.place(x=50, y=HEIGHT//2.5)

        Button(
            start_canvas, text="Start game", font="comicsans 20", command=lambda: self.load_gameui(start_canvas)).place(x=WIDTH//3, y=100)
        Misc.lift(start_canvas)

    def load_gameui(self, canvas):
        self.game.run_game()
        canvas.destroy()
        time.sleep(0.2)
        self.giveup_button["state"] = NORMAL
        self.draw_board()
        self.canvas.bind("<Button-1>", self.clicked)
        self.thread.start()

    def draw_board(self):
        self.draw_grid()
        self.draw_squares()
        self.draw_pieces()
        if self.game.is_game_running():
            self.draw_misc()
        else:
            self.draw_game_end()
        self.update()

    def draw_grid(self):
        for i in range(self.game.rows+1):
            x_start, y_start = MARGIN + i*CELL_WIDTH, MARGIN
            x_end, y_end = MARGIN + i * CELL_WIDTH, HEIGHT-MARGIN

            x_start_h, y_start_h = MARGIN, MARGIN + i*CELL_WIDTH
            x_end_h, y_end_h = WIDTH-MARGIN, MARGIN + i*CELL_WIDTH

            # horizontal lines
            self.canvas.create_line(
                x_start_h, y_start_h, x_end_h, y_end_h, fill="BLACK", width=3)
            # vertical lines
            self.canvas.create_line(
                x_start, y_start, x_end, y_end, fill="BLACK", width=3)

    def draw_squares(self):
        for i in range(self.game.rows):
            for j in range(self.game.columns):
                x_start, y_start = MARGIN+i*CELL_WIDTH, MARGIN+j*CELL_WIDTH
                x_end = MARGIN + i * CELL_WIDTH + CELL_WIDTH
                y_end = MARGIN + j * CELL_WIDTH + CELL_WIDTH
                fill_color = BLACK if (j+i) % 2 else WHITE
                self.canvas.create_rectangle(
                    x_start, y_start, x_end, y_end, fill=fill_color)

    def draw_pieces(self):
        self.canvas.delete("marked-arrow")
        for i in range(self.game.rows):
            for j in range(self.game.columns):
                if self.game.cell_is_piece((i, j)):
                    x, y = self.game.board[i][j].position
                    self.game.board[i][j].draw_self(
                        self.canvas, (MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH//2)
                    if self.game.board[i][j].is_selected():
                        self.canvas.create_oval((MARGIN+x*CELL_WIDTH)+5, (MARGIN+y*CELL_WIDTH)+5,
                                                (MARGIN+x*CELL_WIDTH)+CELL_WIDTH-5, (MARGIN+y*CELL_WIDTH)+CELL_WIDTH-5, outline=SELECTED_COLOR, tag="select_oval")
                    if self.game.board[i][j].get_type() == 5 and self.game.board[i][j].marked:
                        self.canvas.create_line((MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2-1, (MARGIN+y*CELL_WIDTH)+10, (
                            MARGIN+x*CELL_WIDTH)+CELL_WIDTH//2-1, (MARGIN+y*CELL_WIDTH)-15, fill="#ff0000", arrow=FIRST, width=5, tag="marked-arrow")

    def draw_misc(self):
        self.canvas.delete("turn_text")
        self.canvas.create_text(WIDTH//2, HEIGHT-MARGIN//2,
                                text=f"{self.game.turn} Turn".upper(), tag="turn_text", font="comicsans 30")

    def draw_game_end(self):
        self.canvas.delete("turn_text")
        self.canvas.unbind("<Button-1>")
        self.giveup_button["state"] = DISABLED

        end_canvas = Canvas(
            self, width=WIDTH-100, height=HEIGHT//4-20, background=STARTEND_BACKGROUND)
        end_canvas.create_text(WIDTH//2-50, 60,
                               text=f"Winner: {self.game.winner} !".upper(), font="comicsans 36", fill=WHITE)
        end_canvas.place(x=50, y=HEIGHT//2.5)

        Button(
            end_canvas, text="Play again", font="comicsans 20", command=lambda: self.play_again_handler(end_canvas), borderwidth=2).place(x=WIDTH//4-50, y=100)
        Button(
            end_canvas, text="Quit game", font="comicsans 20", command=self.parent.destroy, borderwidth=2).place(x=WIDTH//2, y=100)
        Misc.lift(end_canvas)

    def end_game_handler(self):
        self.game.stop_game("black" if self.game.turn ==
                            "white" else "white")
        self.draw_board()

    def play_again_handler(self, canvas):
        self.game.run_game()
        canvas.destroy()
        time.sleep(0.2)
        self.wtime_label["text"] = f"Time: {self.game.timer_save//60}:00"
        self.btime_label["text"] = f"Time: {self.game.timer_save//60}:00"
        self.giveup_button["state"] = NORMAL
        self.draw_board()
        self.canvas.bind("<Button-1>", self.clicked)
        try:
            self.thread.start()
        except RuntimeError:
            pass

    def update_timer(self):
        if self.game.turn == "white":
            timer = self.format_time(self.game.white_time)
            self.wtime_label["text"] = timer
            self.game.white_time -= 1
        else:
            timer = self.format_time(self.game.black_time)
            self.btime_label["text"] = timer
            self.game.black_time -= 1
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
            self.end_game_handler()
        return formatted_string

    def initiate_piece_move(self, x, y):
        piece = self.game.get_selected_piece()
        if piece is not None:
            if not piece.get_type() == 5:  # if it's not a king
                valid_moves = piece.get_valid_moves(self.game)
                if (x, y) in valid_moves:
                    self.game.handle_piece_move(
                        piece, (x, y))
            else:  # if it's a king, we have to check the normal and castle moves
                valid_kingmoves, valid_castle_moves = piece.get_valid_moves(
                    self.game)
                if (x, y) in valid_kingmoves:
                    self.game.handle_piece_move(
                        piece, (x, y))
                elif len(valid_castle_moves) > 0 and ((x, y) == valid_castle_moves[0][1] or (x, y) == valid_castle_moves[1][1]):
                    if (x, y) == valid_castle_moves[0][1]:
                        self.game.handle_castle_move(
                            piece, valid_castle_moves[0])
                    else:
                        self.game.handle_castle_move(
                            piece, valid_castle_moves[1])
            try:
                self.thread.start()
            except RuntimeError:
                pass
            self.draw_board()
        # do nothing if no piece is selected

    def clicked(self, event):
        x, y, = event.x, event.y
        if MARGIN < x < WIDTH-MARGIN and MARGIN < y < WIDTH-MARGIN:  # if we clicked on the game-game
            x_grid_pos = int(x//CELL_WIDTH-1)
            y_grid_pos = int(y//CELL_WIDTH-1)
            # if we clicked on a piece
            if self.game.cell_is_piece((x_grid_pos, y_grid_pos)):
                # if turn and piece color match
                if self.game.board[x_grid_pos][y_grid_pos].player == self.game.turn:
                    # it the piece is selected...
                    if self.game.board[x_grid_pos][y_grid_pos].is_selected():
                        self.game.board[x_grid_pos][y_grid_pos].unselect(
                        )  # ...we unselect it
                    # if the piece is not selected...
                    else:
                        # ... we unselect every other piece
                        self.game.unselect_all()
                        self.canvas.delete("select-oval")
                        # and select the new one
                        self.game.board[x_grid_pos][y_grid_pos].select()
                    self.draw_board()
                # if turn and color don't match
                else:
                    self.initiate_piece_move(x_grid_pos, y_grid_pos)
            # we clicked on a free cell
            else:
                self.initiate_piece_move(x_grid_pos, y_grid_pos)
