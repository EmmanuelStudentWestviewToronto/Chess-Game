from .piece import Piece
from tkinter import PhotoImage


class Rook(Piece):
    def __init__(self, x, y, player):
        super().__init__(x=x, y=y, player=player)
        self.type = 3
        self.set_image()

    def set_image(self):
        color_num = 0 if self.player == "white" else 1
        self.image = f"img\\{color_num}0{self.type}.png"

    def move(self, destination):
        self.position = destination

    def is_valid_move(self, destination):
        x_destination, y_destination = destination

    def draw_path(self, start, end):
        x_start, y_start = start
        x_end, y_end = end

    def draw_self(self, canvas, x, y):
        img = PhotoImage(file=self.image)
        canvas.create_image(x, y, image=img)
        self.image = img
