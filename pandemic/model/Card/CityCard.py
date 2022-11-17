from pandemic.model.Card.Card import Card
from pandemic.model.City import City


class CityCard(Card):

    def __init__(self, city: City):
        self.city: City = city

    def __str__(self):
        return f'Card({self.city.name})'

    def __repr__(self):
        return self.__str__()
