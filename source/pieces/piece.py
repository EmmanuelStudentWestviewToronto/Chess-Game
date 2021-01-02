from abc import ABC, abstractmethod
from tkinter import PhotoImage


class Piece(ABC):
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        """ type = int from 0-5
        0 = Pawn, 1 = Knight, 2 = Bishop, 3 = Rook, 4 = Queen, 5 = King
        -1 = None
        """
        self.type = -1
        self.player = player
        self.image = None
        self.image_garbo = None
        self.selected = False
        self.move_counter = 0  # for castle moves

    @abstractmethod
    def get_valid_moves(self, board):
        pass

    @abstractmethod
    def set_image(self):
        pass

    def draw_self(self, canvas, x, y):
        img = PhotoImage(file=self.image)
        canvas.create_image(x, y, image=img)
        self.image_garbo = img

    def get_type(self):
        return self.type

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def is_selected(self):
        return True if self.selected else False

    def move(self, destination):
        self.position = destination
        self.x, self.y = self.position
        self.unselect()
        self.move_counter += 1
