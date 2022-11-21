import random
from typing import Any

from pandemic.model.Action.Action import Action
from pandemic.model.Action.MoveToNeighborCity import MoveToNeighborCity
from pandemic.models import City


class DummyInputView:
    @staticmethod
    def get_action() -> (Action, Any):
        return MoveToNeighborCity(), random.choice(City.objects.all())
