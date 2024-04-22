from Handler.Handler import Handler
from Generation.TestRunner import TestRunner
from Helper.TerminalPrinter import TerminalPrinter
from File.FileSanitiser import FileSanitiser
from Generation.Result import Result

"""
This class is a handler for the Human constructed tests. It handles initiating
the unit tests and mutation testing
"""

class HumanHandler(Handler):

    CSV_HEADERS: list = [
        "HUMAN_mutation_score",
        "HUMAN_code_coverage"
        ]

    def __init__(self, 
                result : Result,
                test_runner : TestRunner, 
                class_name: str,
                original_test_path: str,
                original_class_path: str
            ) -> None:
        self.result = result
        self.test_runner: TestRunner = test_runner
        self.file_sanatiser = FileSanitiser()
        self.class_name = class_name
        self.original_test_path = original_test_path
        self.original_class_path = original_class_path
        self.printer = TerminalPrinter()

    @classmethod
    def get_csv_headers(cls):
        """
        Return the headers used in CSV file. Must be overriden from ABC
        """
        return cls.CSV_HEADERS
    
    def execute(self):

        test_output = self.test_runner.run_unit_test(self.original_test_path)
        
        # The subprocess timed out or threw an exception
        if test_output is None:
            self.result.values.append("Error")
            self.result.values.append("Error")
            return

        overview_tuple, _ = self.test_runner.run_mutation_test(self.original_test_path, self.class_name, self.result, self.original_class_path)

        # The overview tuple was None.
        if overview_tuple is None:
            self.result.values.append("NoReport")
            self.result.values.append("NoReport")
            self.printer.print_with_color("NoReport", "yellow")
            return

        self.printer.print_with_color(overview_tuple, "yellow")

        # Update result object
        self.result.values.append(overview_tuple.mutation_score_percent)
        self.result.values.append(overview_tuple.code_coverage_percent)