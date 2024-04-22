from abc import ABC, abstractmethod

"""
Abstract class for handlers
"""

class Handler(ABC):

    @abstractmethod
    def execute(): pass

    @abstractmethod
    def get_csv_headers(): pass

    