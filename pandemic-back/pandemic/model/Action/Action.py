from abc import ABC, abstractmethod

from pandemic.model.World import World


class Action(ABC):

    @abstractmethod
    def execute_action(self, world, arg) -> bool:
        pass
