import os
from typing import List

from pandemic.model.Card.Card import Card
from pandemic.model.Card.EpidemicCard import EpidemicCard
from pandemic.model.City import City
from pandemic.model.Card.CityCard import CityCard
from pandemic.model.Color import Color
from pandemic.model.Player import Player


class World:

    def __init__(self,
                 cities: List[City],
                 players: List[Player],
                 player_cards: List[Card],
                 disease_cards: List[CityCard]):
        self.cities: List[City] = cities
        self.players: List[Player] = players
        self.player_cards: List[Card] = player_cards
        self.disease_cards: List[CityCard] = disease_cards

        self.discard_disease_cards = []
        self.number_of_outbreak: int = 0
        self.spreading_rates: List[int] = [2, 2, 2, 3, 3, 4, 4]
        self.current_spreading_rate = 0
        self.is_antidote_found: dict[Color, bool] = {
            Color.YELLOW: False,
            Color.BLACK: False,
            Color.BLUE: False,
            Color.RED: False,
        }

    @property
    def spreading_rate(self) -> int:
        return self.spreading_rates[self.current_spreading_rate]

    @property
    def current_player(self) -> Player:
        return self.players[0]

    def __str__(self):
        return f'''
World:
    Cities: 
{os.linesep.join(map(lambda x: "        "+str(x), self.cities))}
    Players: {self.players}
    Player cards: {len(self.player_cards)}
    Disease cards: {len(self.discard_disease_cards)}|{len(self.disease_cards)}
    Spreading rate: {self.spreading_rate}
    Antidote found: {list(map(lambda x: x[0], filter(lambda x: x[1], self.is_antidote_found.items())))}
        '''
