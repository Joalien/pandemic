from typing import List, Callable

from pandemic.model.Action.Action import Action
from pandemic.models import City, CityCard, World


class MoveTowardCity(Action):

    def execute_action(self, world, arg) -> bool:
        player = world.current_player  # will not work, to refactor
        city_card_in_player_hand = list(filter(lambda x: isinstance(x, CityCard), player.hand))
        current_position_or_destination = lambda city_card: city_card == player.city or city_card == arg
        # FIXME quite dirty
        try:
            city_card_to_play = next(filter(current_position_or_destination, city_card_in_player_hand))
            if isinstance(arg, City):
                player.city = arg
                player.hand.remove(city_card_to_play)
        except StopIteration:
            pass
        return False
