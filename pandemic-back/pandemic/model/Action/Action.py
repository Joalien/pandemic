from abc import ABC
from typing import Tuple


class Action(ABC):

    @staticmethod
    def execute_action(**kwargs) -> Tuple[bool, str]:
        pass
