# svc.py
from abc import ABC, abstractmethod

class Svc(ABC):
    @abstractmethod
    def write(self, text: str) -> None:
        pass
