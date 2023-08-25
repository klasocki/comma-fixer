from abc import ABC, abstractmethod


class CommaFixerInterface(ABC):
    @abstractmethod
    def fix_commas(self, s: str) -> str:
        pass
