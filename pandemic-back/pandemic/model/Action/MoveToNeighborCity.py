from typing import Any

from pandemic.View.OutputView.OutputView import OutputView
from pandemic.model.Action.Action import Action
from pandemic.model.City import City
from pandemic.model.World import World


class MoveToNeighborCity(Action):

    def execute_action(self, world, arg: Any):
        if isinstance(arg, City) and arg in world.current_player.position.neighbors:
            OutputView.INSTANCE.show_message(f'Moving from {world.current_player.position.name} to {arg.name}')
            world.current_player.position = arg
            return True
        return False
