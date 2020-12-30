from abc import ABC, abstractmethod


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

    @abstractmethod
    def is_valid_move(self, destination):
        pass

    @abstractmethod
    def draw_path(self, start, end):
        pass

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
