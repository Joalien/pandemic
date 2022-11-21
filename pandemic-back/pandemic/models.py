from __future__ import annotations

import os
from enum import Enum, auto
from typing import Tuple, List

from django.db import models
from django.db.models.signals import post_init


class Color(models.TextChoices):
    YELLOW = auto()
    BLUE = auto()
    BLACK = auto()
    RED = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Player(models.Model):
    name = models.CharField(max_length=50)
    position = models.ForeignKey('City', on_delete=models.CASCADE, related_name='players_in_city')
    world = models.ForeignKey('World', on_delete=models.CASCADE, related_name='players')
    next_player = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='+')

    # def __init__(self, name: str, position: City, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.name: str = name
    #     self.position: City = position
    #     self.hand: List[Card] = []

    def __str__(self):
        return f'{self.name} ({self.position.name}) has {self.hand}'

    def __repr__(self):
        return self.__str__()


class Card(models.Model):
    city: City = models.ForeignKey('City', null=True, default=None, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=50, null=True, default=None)
    index = models.IntegerField(null=False)

    def __str__(self):
        return f'Card({self.name if self.name is not None else self.city.name})'

    def __repr__(self):
        return self.__str__()


class PlayerCard(Card):
    world = models.ForeignKey('World', on_delete=models.CASCADE, related_name='player_cards')
    player = models.ForeignKey(Player, null=True, default=None, on_delete=models.CASCADE, related_name='hand')


class DiseaseCard(Card):
    world = models.ForeignKey('World', on_delete=models.CASCADE, related_name='disease_cards')
    is_discarded = models.BooleanField(default=False)


class CheatCard(PlayerCard):
    pass


class EpidemicCard(PlayerCard):
    pass


def default_city_diseases():
    return {
        Color.YELLOW.name: 0,
        Color.BLACK.name: 0,
        Color.BLUE.name: 0,
        Color.RED.name: 0,
    }


def default_position():
    return {'x': 0, 'y': 0}


class City(models.Model):
    world = models.ForeignKey('World', on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50)
    color = models.CharField(choices=Color.choices, max_length=50)
    has_research_center = models.BooleanField(default=False)
    neighbors = models.ManyToManyField("self")
    diseases = models.JSONField(default=default_city_diseases)
    position = models.JSONField(default=default_position)

    # def init(self, id, name: str, color: Color, position: (Tuple[int, int]), *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.name: str = name
    #     self.color: Color = color
    #     self.has_research_center = False
    #     self.position = position
    #     # self.neighbors = []
    #     self.diseases: dict[Color, int] = {
    #         Color.YELLOW.name: 0,
    #         Color.BLACK.name: 0,
    #         Color.BLUE.name: 0,
    #         Color.RED.name: 0,
    #     }

    def add_neighbors(self, *neighbors: City):
        pass
        # [self.neighbors.add(c) for c in neighbors]

    def construct_research_center(self):
        self.has_research_center = True
        self.save()

    def __str__(self):
        return f'{self.name.ljust(12)}{self.diseases}{" (DATA_CENTER)" if self.has_research_center else ""}'

    def __repr__(self):
        return self.__str__()


def default_antidotes():
    return {
        Color.YELLOW: False,
        Color.BLACK: False,
        Color.BLUE: False,
        Color.RED: False,
    }


class World(models.Model):
    number_of_outbreak = models.IntegerField(default=0)
    current_spreading_rate = models.IntegerField(default=0)
    spreading_rates: List[int] = [2, 2, 2, 3, 3, 4, 4]
    are_antidotes_found = models.JSONField(default=default_antidotes)
    current_player = models.OneToOneField('Player', null=True, on_delete=models.CASCADE, related_name='+')

    # def __init__(self, cities: List[City],
    #              players: List[Player],
    #              player_cards: List[Card],
    #              disease_cards: List[CityCard],
    #              *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.cities: List[City] = cities
    #     self.players: List[Player] = players
    #     self.player_cards: List[Card] = player_cards
    #     self.disease_cards: List[CityCard] = disease_cards
    #
    #     self.discard_disease_cards = []
    #     self.number_of_outbreak: int = 0
    #     self.spreading_rates: List[int] = [2, 2, 2, 3, 3, 4, 4]
    #     self.current_spreading_rate = 0
    #     self.is_antidote_found: dict[Color, bool] = {
    #         Color.YELLOW: False,
    #         Color.BLACK: False,
    #         Color.BLUE: False,
    #         Color.RED: False,
    #     }

    @property
    def spreading_rate(self) -> int:
        return self.spreading_rates[self.current_spreading_rate]

    # @property
    # def current_player(self) -> Player:
    #     return self.players[0]

    def __str__(self):
        return f'''
World:
    Cities: 
{os.linesep.join(map(lambda x: "        " + str(x), self.cities.all()))}
    Players: {self.players.all()}
    Player cards: {len(self.player_cards.all())}
    Disease cards: {len([c for c in self.disease_cards.all() if c.is_discarded])}|{len([c for c in self.disease_cards.all() if not c.is_discarded])}
    Spreading rate: {self.spreading_rate}
    Antidote found: {list(map(lambda x: x[0], filter(lambda x: x[1], self.are_antidotes_found.items())))}
        '''


class OutOfDiseaseCardError(Exception):
    pass


class OutOfPlayerCardError(Exception):
    pass
