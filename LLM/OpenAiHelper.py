import tiktoken

"""
This class provides functions to ensure the GPT model runs smoothly
"""

class OpenAiHelper():

    context_length: dict = {
        "gpt-3.5-turbo-1106": 16000
    }

    completion_length: dict = {
        "gpt-3.5-turbo-1106": 4096
    }

    def __init__(self, base_model):
        self.base_model = base_model
        self.encoder = tiktoken.encoding_for_model(base_model)

    
    def is_completion_overflow(self, content):
        """
        Check whether token length of the chat completion is within the allowed amount the specific
        """
        return len(self.encoder.encode(content)) >= self.completion_length.get(self.base_model)


    def is_context_overflow(self, content):
        """
        Check whether token length of the context is within the allowed amount the specific
        model, which is (context length - completion length)
        """
        current_context = len(self.encoder.encode(content))

        return len(self.encoder.encode(content)) >= (self.context_length.get(self.base_model)-(self.completion_length.get(self.base_model)))

    def is_training_data_overflow(self, content):
        """
        Check to make sure conte
        """
        return len(self.encoder.encode(content)) <= (self.completion_length.get(self.base_model) * 2)
