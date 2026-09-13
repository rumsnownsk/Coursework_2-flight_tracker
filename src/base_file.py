from abc import ABC, abstractmethod
from pathlib import Path


class BaseFile(ABC):

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    @abstractmethod
    def write_to_file(self, data):
        pass

    @abstractmethod
    def add_aeroplane(self):
        pass

    @abstractmethod
    def read_from_file(self):
        pass

    @abstractmethod
    def delete_aeroplane(self):
        pass