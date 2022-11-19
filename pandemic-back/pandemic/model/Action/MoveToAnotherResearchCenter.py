from typing import List, Callable

from pandemic.model.Action.Action import Action
from pandemic.model.Card.CityCard import CityCard
from pandemic.model.City import City
from pandemic.model.World import World


class MoveToAnotherResearchCenter(Action):

    def execute_action(self, world, arg) -> bool:
        if isinstance(arg, City) and world.current_player.position.has_research_center and arg.has_research_center:
            world.current_player.position = arg
            return True
        return False