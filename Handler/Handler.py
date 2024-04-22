from abc import ABC, abstractmethod

class Handler(ABC):

    @abstractmethod
    def execute(): pass

    @abstractmethod
    def get_csv_headers(): pass

    