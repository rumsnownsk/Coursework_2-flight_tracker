from abc import ABC, abstractmethod


class BaseApi(ABC):

    @abstractmethod
    def get_aeroplanes(self, country):
        pass