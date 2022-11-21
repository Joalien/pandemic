from __future__ import annotations

from abc import abstractmethod


class OutputView:
    INSTANCE: OutputView

    @abstractmethod
    def show_message(self, message: str) -> None:
        pass
