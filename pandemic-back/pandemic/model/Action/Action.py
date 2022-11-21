from abc import ABC, abstractmethod


class Action(ABC):

    @abstractmethod
    def execute_action(self, world, arg) -> bool:
        pass
