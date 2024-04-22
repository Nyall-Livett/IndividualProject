from Handler.Handler import Handler
from LLM.ChatGptModelTuned import ChatGptModelTuned, ILanguageModel 
from Generation.TestRunner import TestRunner
from File.FileIO import FileIO
from Helper.TerminalPrinter import TerminalPrinter
from File.FileSanitiser import FileSanitiser
from Generation.Result import Result
import re


class LLM2Handler(Handler):

    TEST_ERROR_LOOP_COUNT: int = 5
    TEST_GENERATION_PASS_COUNT: int = 2

    ERROR_CODE: int = 1

    generation_successful : bool = False

    CSV_HEADERS: list = [
        "LLM2_code_coverage_1",
        "LLM2_mutation_score_1",
        "LLM2_code_coverage_2",
        "LLM2_mutation_score_2"
    ]

    def __init__(self, 
                result : Result,
                test_runner : TestRunner, 
                class_content: str, 
                class_name: str,
                original_test_path: str,
                original_class_path: str,
                original_test_file: str
                ) -> None:
        self.LLM: ILanguageModel = ChatGptModelTuned("ft:gpt-3.5-turbo-1106:personal::9EJVwdWC:ckpt-step-1480")
        self.file_io = FileIO()
        self.file_sanatiser = FileSanitiser()
        self.printer = TerminalPrinter()
        self.result = result
        self.class_content = class_content
        self.class_name = class_name
        self.original_test_path = original_test_path
        self.test_runner: TestRunner = test_runner
        self.original_class_path = original_class_path
        self.original_test_file = original_test_file

    @classmethod
    def get_csv_headers(cls):
        """
        Return the headers used in CSV file. Must be overriden from ABC
        """
        return cls.CSV_HEADERS

    def _reached_limit(self, current_count):
        return current_count >= self.TEST_ERROR_LOOP_COUNT-1


    def _print_iteration_details(self, count):
        print(f"Generating test for {self.class_name} - attempt {count+1}/{self.TEST_ERROR_LOOP_COUNT}")


    def execute(self):
        """
        DISABLED
        """
        self.result.values.append("NoReport")   
        self.result.values.append("NoReport")
        return

    def generate_test_suite(self, prompt):
        """
        Generate code from LLM, allowing retries if there are errors in the code. 
        It also allows a complete retry
        """

        for count in range(self.TEST_ERROR_LOOP_COUNT):
            self._print_iteration_details(count)
            
            generated_content = self.LLM.generate_test_case(prompt)

            # Was an issue with LLM context window or OpenAI API
            if generated_content is None:
                return None
                
            # Overwrite the code in the original file with the new code.
            self.file_io.write_file_from_string(self.original_test_path, generated_content)

            # Run the test and receive the Standard output, whether it failed or not
            # test_output could be None if there was an exception otherwise it will be std.out
            test_output = self.test_runner.run_unit_test(self.original_test_path)

            # The subprocess timed out or threw an exception
            if test_output is None:
                if self._reached_limit(count):
                    return None
                continue
            
            # Errors within the standard output.
            if test_output.returncode == self.ERROR_CODE:
                
                # Return false after limit of error
                if self._reached_limit(count):
                    return None
                
                self.printer.print_with_color("Error while executing unit test \nFeeding back to LLM to try and rectify" , "red")
                error_message = self.extract_error_info(test_output.stdout)

                # If could not extract error message, simply feed the std.out in
                # This could lead to worse outcome depending on how many tokens it use up
                if error_message is None:
                    error_message = test_output.stdout

                prompt = self.LLM.generate_error_propmt(error_message)

                continue
            return True
        

    def extract_error_info(self, stdout):
        """
        Extracts compilation error information from stdout.
        """
        self.printer.print_with_color("Extracting error information", "yellow")
        # Define start and end patterns
        start_pattern = r"\[ERROR\] COMPILATION ERROR :"
        end_pattern = r"\[INFO\] Total time:"

        # Compile regex patterns for efficiency if called multiple times
        start_regex = re.compile(start_pattern)
        end_regex = re.compile(end_pattern)

        # Find the start and end using the compiled regex
        start_match = start_regex.search(stdout)
        end_match = end_regex.search(stdout)

        # If both start and end are found, extract the content between them
        if start_match and end_match:
            start_index = start_match.end()  # End of the start marker
            end_index = end_match.start()  # Start of the end marker
            error_info = stdout[start_index:end_index].strip()
            return error_info
        else:
            self.printer.print_with_color("No compilation error, feeding STDOUT instead of condensed error report", "red")
            return stdout

    def _is_perfect_score(self, score):
        """
        Checks to see if the scores are both 100 and returns True otherwise returns False
        """
        if score.mutation_score_percent == 100 and score.code_coverage_percent == 100:
            return True
        
        return False