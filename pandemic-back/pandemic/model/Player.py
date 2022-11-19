from typing import List

from pandemic.model.Card.Card import Card
from pandemic.model.City import City


class Player:

    def __init__(self, name: str, position: City):
        self.name: str = name
        self.position: City = position
        self.hand: List[Card] = []

    def __str__(self):
        return f'{self.name} ({self.position.name}) has {self.hand}'

    def __repr__(self):
        return self.__str__()
