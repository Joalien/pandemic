from typing import Tuple

from pandemic.model.Action.Action import Action
from pandemic.models import City, Player
from pandemic.view.OutputView.OutputView import OutputView


class MoveToNeighborCity(Action):

    @staticmethod
    def execute_action(**kwargs) -> Tuple[bool, str]:
        city = kwargs['city']
        player = kwargs['player']
        if isinstance(city, City) and isinstance(player, Player) and city in player.city.neighbors.all():
            OutputView.INSTANCE.show_message(f'Moving from {player.city.name} to {city.name}')
            player.city = city
            player.save()
            return True, ''
        return False, f'Player cannot move to city {city.name}'
