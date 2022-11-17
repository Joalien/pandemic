from enum import Enum, auto


class Color(Enum):

    YELLOW = auto()
    BLUE = auto()
    BLACK = auto()
    RED = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
