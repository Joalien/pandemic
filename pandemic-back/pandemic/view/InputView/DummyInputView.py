import random
from typing import Any

from pandemic.model.Action.Action import Action
from pandemic.model.Action.MoveToNeighborCity import MoveToNeighborCity
from pandemic.models import City, Player


class DummyInputView:
    @staticmethod
    def get_action(**kwargs) -> (Action, Any):
        return MoveToNeighborCity(), random.choice(Player.objects.filter(world=kwargs['world']).first().position.neighbors.all())
