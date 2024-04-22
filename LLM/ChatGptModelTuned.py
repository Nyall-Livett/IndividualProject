from LLM.ILanguageModel import ILanguageModel
from openai import OpenAI
from LLM.OpenAiHelper import OpenAiHelper
from Helper.TerminalPrinter import TerminalPrinter
from Config import Config

class ChatGptModelTuned(ILanguageModel):

    CLIENT = OpenAI(api_key=Config.get_key())
    CHAT_LOG: list = [{"role": "system", "content": "Welcome to the Automated Java Testing Service! Please submit your Java code below"}]
    
    def __init__(self, model):
        self.printer = TerminalPrinter()
        self.model = model
        self.open_ai_helper = OpenAiHelper("gpt-3.5-turbo-1106")

    def generate_initial_prompt(self, class_content: str):
        """
        Create a new message for the initial test generation, insert the class content
        into the message and return it
        """
        return f"Given the following Java code, show me comprehensive unit tests using JUnit. Ensure the tests cover all functions adequately, including edge cases and typical use cases.  Response should be written in Java code only, no additional words. Here is the Java code: {class_content}"

    def generate_error_propmt(self, error_message: str):
        """
        Create a new message for when there has been a error, insert the error
        message into the message and return it
        """
        return f"Fix these errors from the generated test cases {error_message}"

    def generate_mutation_prompt(self, mutation_report: str):
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

    def generate_test_case(self, message):
        """
        Make a request to OpenAi api to generate a test case and return it.
        """
        self.CHAT_LOG.append({"role": "user", "content": message})
        self.prune_chat_log()
        print(f"Generating for {self.model}")
        if len(self.CHAT_LOG) == 0 or (len(self.CHAT_LOG) + 2048) >= 16384:
            return None
        try:
            response = self.CLIENT.chat.completions.create(
                model=self.model,
                temperature=0.8,
                top_p=0.9,
                frequency_penalty=0,
                presence_penalty=0,
                max_tokens=2048,
                messages=self.CHAT_LOG
            )
            
        except KeyboardInterrupt:
            print("User cancelled the operation.")
            raise
        except:
            self.printer.print_with_color("Error while contacting OpenAI API", "red")
            return None

        generated_content = response.choices[0].message.content        
        self.CHAT_LOG.append({"role": "assistant", "content": generated_content})
        return generated_content


