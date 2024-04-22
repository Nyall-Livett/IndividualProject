from abc import ABC, abstractmethod

"""
Abstract class for Language models
"""

class ILanguageModel(ABC):

    @abstractmethod
    def prune_chat_log(message):
        pass

    @abstractmethod
    def generate_initial_prompt(class_content) -> str:
        pass

    @abstractmethod
    def generate_error_propmt(error_message) -> str:
        pass

    @abstractmethod
    def generate_mutation_prompt(report) -> str:
        pass

    @abstractmethod
    def generate_test_case(message) -> str:
        pass

    @abstractmethod
    def restart_chat_log():
        pass