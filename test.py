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
        super().__init__()

    @abstractmethod
    def move(self, destination):
        pass

    @abstractmethod
    def is_valid_move(self, destination):
        pass

    @abstractmethod
    def draw_path(self, start, end):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def set_image(self):
        pass


class Rook(Piece):

    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.type = 3
        self.set_image()

    def set_image(self):
        color_num = 0 if self.player == "white" else 1
        self.image = f"img/{color_num}0{self.type}.png"

    def move(self, destination):
        # todo check if valid
        self.position = destination

    def is_valid_move(self, destination):
        x_destination, y_destination = destination

    def draw_path(self, start, end):
        x_start, y_start = start
        x_end, y_end = end

    def get_type(self):
        return self.type


rook = Rook(1, 1, "white")
rook2 = Rook(3, 5, "black")
print(rook2.image)
