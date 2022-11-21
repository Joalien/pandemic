from pandemic.model.Action.Action import Action
from pandemic.models import City, Player
from pandemic.view.OutputView.OutputView import OutputView


class MoveToNeighborCity(Action):

    @staticmethod
    def execute_action(**kwargs) -> bool:
        city = kwargs['city']
        player = kwargs['player']
        if isinstance(city, City) and isinstance(player, Player) and city in player.position.neighbors.all():
            OutputView.INSTANCE.show_message(f'Moving from {player.position.name} to {city.name}')
            player.position = city
            player.save()
            return True
        return False
