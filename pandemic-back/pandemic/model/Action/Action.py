from abc import ABC


class Action(ABC):

    @staticmethod
    def execute_action(**kwargs) -> bool:
        pass
