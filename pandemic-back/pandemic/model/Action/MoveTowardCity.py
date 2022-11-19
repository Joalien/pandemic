from typing import List, Callable

from pandemic.model.Action.Action import Action
from pandemic.model.Card.CityCard import CityCard
from pandemic.model.City import City
from pandemic.model.World import World


class MoveTowardCity(Action):

    def execute_action(self, world, arg) -> bool:
        player = world.current_player
        city_card_in_player_hand = list(filter(lambda x: isinstance(x, CityCard), player.hand))
        current_position_or_destination = lambda city_card: city_card == player.position or city_card == arg
        # FIXME quite dirty
        try:
            city_card_to_play = next(filter(current_position_or_destination, city_card_in_player_hand))
            if isinstance(arg, City):
                player.position = arg
                player.hand.remove(city_card_to_play)
        except StopIteration:
            pass
        return False
