from typing import Any

from pandemic.view.OutputView.OutputView import OutputView
from pandemic.model.Action.Action import Action
from pandemic.models import City, World


class MoveToNeighborCity(Action):

    def execute_action(self, world, arg: Any) -> bool:
        if isinstance(arg, City) and arg in world.current_player.position.neighbors.all():
            OutputView.INSTANCE.show_message(f'Moving from {world.current_player.position.name} to {arg.name}')
            world.current_player.position = arg
            return True
        return False
