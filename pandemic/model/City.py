from __future__ import annotations

from typing import List

from pandemic.model.Color import Color


class City:
    cities: List[City] = []

    def __init__(self, name: str, color: Color):
        self.name: str = name
        self.color: Color = color
        self.has_research_center = False
        self.neighbors: List[City] = []
        self.diseases: dict[Color, int] = {
            Color.YELLOW: 0,
            Color.BLACK: 0,
            Color.BLUE: 0,
            Color.RED: 0,
        }
        self.__class__.cities.append(self)

    def add_neighbors(self, *neighbors: City):
        [self.neighbors.append(c) for c in neighbors]

    def construct_research_center(self):
        self.has_research_center = True

    def __str__(self):
        return f'{self.name.ljust(12)}{self.diseases}{" (DATA_CENTER)" if self.has_research_center else ""}'

    def __repr__(self):
        return self.__str__()

