from abc import ABC, abstractmethod
from pathlib import Path

from src.aeroplane import Aeroplane


class BaseFile(ABC):

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    @abstractmethod
    def write_to_file(self, data):
        pass

    @abstractmethod
    def add_aeroplane(self, *args, **kwargs) -> None:
        """Добавить самолёт в хранилище."""
        pass

    @abstractmethod
    def read_from_file(self):
        pass

    @abstractmethod
    def delete_aeroplane(self, id_flight:str) -> str:
        """Удалить самолёт по id_flight."""
        pass
