from LLM.ILanguageModel import ILanguageModel
from openai import OpenAI
from LLM.OpenAiHelper import OpenAiHelper
from Helper.TerminalPrinter import TerminalPrinter

class ChatGptModelTuned(ILanguageModel):

    CLIENT = OpenAI(api_key="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")
    CHAT_LOG: list = [{"role": "system", "content": "Welcome to the Automated Java Testing Service! Please submit your Java code below"}]
    TRAINED_MODEL = "ft:gpt-3.5-turbo-1106:personal::9BRUtgN7"
    
    def __init__(self):
        self.printer = TerminalPrinter()
        base_model = "ft:gpt-3.5-turbo-1106:personal::9BRUtgN7".split(":")[1] 
        self.open_ai_helper = OpenAiHelper(base_model)

    def generate_test_for_initial(self, class_content: str):
        """
        Create a new message for the initial test generation, insert the class content
        into the message and return it
        """
        return f"Given the following Java code, show me comprehensive unit tests using JUnit. Ensure the tests cover all functions adequately, including edge cases and typical use cases.  Response should be written in Java code only, no additional words. Here is the Java code: {class_content}"

    def generate_test_for_error_message(self, error_message: str):
        """
        Create a new message for when there has been a error, insert the error
        message into the message and return it
        """
        return f"Fix these errors from the generated test cases {error_message}"

    def generate_test_for_mutation_message(self, mutation_report: str):
        """
        Create a new message for when there has been a error, insert the error
        message into the message
        """
        return f"Using this report, improve the tests cases you have generated {mutation_report}"
    
    def restart_chat_log(self):
        """
        Restart chat log for new test case
        """
        self.CHAT_LOG : list = [{"role": "system", "content": "TestGen can generate units when given a class"}]

    def prune_chat_log(self):
        """
        Checks to see if the next message appended to the chat log would exceed the context 
        window of the base GPT model and removes the head of the list if so.
        """        
        while self.open_ai_helper.is_context_overflow(str(self.CHAT_LOG)):
            self.CHAT_LOG.pop(0)

    def print_context_space(self):
        """
        Prints the used and remaining space in the GPT context window
        """
        self.printer.print_with_color(self.open_ai_helper.calculate_context_space_as_string(str(self.CHAT_LOG)), "yellow")
        

    def generate_test_case(self, message):
        """
        Make a request to OpenAi api to generate a test case and return it.
        """
        self.CHAT_LOG.append({"role": "user", "content": message})
        self.prune_chat_log()
        
        if len(self.CHAT_LOG) == 0:
            return None

        response = self.CLIENT.chat.completions.create(
            model=self.TRAINED_MODEL,
            temperature=0.5,
            top_p=0.8,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=4096, # How many tokens the response can be
            messages=self.CHAT_LOG
        )

        generated_content = response.choices[0].message.content        
        self.CHAT_LOG.append({"role": "assistant", "content": generated_content})
        self.print_context_space()
        return generated_content


