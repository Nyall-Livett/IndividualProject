from pathlib import Path
from CommandCenters.BuildSystemEnum import BuildSystem
from File.FileIO import FileIO
from collections import namedtuple
from Parser.HTMLParser import HTMLParser
from Parser.XMLParser import XMLParser
from Helper.TerminalPrinter import TerminalPrinter
from Generation.Result import Result
from pathlib import Path
import shutil


"""
This class handles extracting mutation testing data from the project
"""

class MutationDataHandler():

    PITEST_HTML_REPORT_FOLDER: str = None
    MAVEN_PITEST_MAIN_REPORT_FOLDER: str = "target/pit-reports/"
    INDEX: str = "index.html"
    MUTATIONS: str = "mutations.xml"

    def __init__(self, build_system, module_dir, package_name, result_statistics_obj: Result):
        self.file_io = FileIO()
        self.printer = TerminalPrinter()
        self.result_statistics_obj = result_statistics_obj
        self.__compose_html_report_folder(module_dir, build_system, package_name)
        self.__compose_xml_report_folder(module_dir, build_system)


    def __compose_html_report_folder(self, module_dir, build_system, package_name):
        """
        Composes the correct file path to the Pitest report folder depending on the build and
        the module path. This folder contains the HTML that has mutation score and code coverage.
        """
        if build_system == BuildSystem.MAVEN:
            self.PITEST_HTML_REPORT_FOLDER = Path(module_dir, self.MAVEN_PITEST_MAIN_REPORT_FOLDER, package_name)
   

    def __compose_xml_report_folder(self, module_dir, build_system):
        """
        Composes the correct file path to the Pitest report folder depending on the build and
        the module path. This folder contains the HTML that has mutation score and code coverage.
        """
        if build_system == BuildSystem.MAVEN:
            self.PITEST_XML_REPORT_FOLDER = Path(module_dir, self.MAVEN_PITEST_MAIN_REPORT_FOLDER)
   

    def _extract_overview_coverage(self, class_name):
        """
        Extract the overview scores from the pitest report which consists of mutation score, code
        coverage and test strength
        """
        index_path = Path(self.PITEST_HTML_REPORT_FOLDER, self.INDEX)
        
        pitest_index_as_string = self.file_io.read_file_as_string(index_path)

        # Could not find the file or there was an exception
        if pitest_index_as_string is None:
            return None

        parser = HTMLParser(pitest_index_as_string, self.result_statistics_obj)

        # Ret could be None if the class couldnt be found in the mutation report
        ret = parser.extract_mutation_scores(class_name)
        return ret
    

    def delete_folder(self):
        """
        Remove the pitest folder
        """
        # Make sure there are no old results left behind that may intefere with the integrity of results.
        # For instance if one is successful and the new round is not, when it goes to read the results 
        # it will find the old ones still there as if they are new.
        if self.PITEST_XML_REPORT_FOLDER.exists() and self.PITEST_XML_REPORT_FOLDER.is_dir():
            shutil.rmtree(self.PITEST_XML_REPORT_FOLDER)
        

    def _extract_living_mutants(self, class_name):
        """
        Extract the living mutants from the pitest report which consists of any mutants still 
        alive
        """
        index_path = Path(self.PITEST_XML_REPORT_FOLDER, self.MUTATIONS)
        pitest_index_as_string = self.file_io.read_file_as_string(index_path)

        parser = XMLParser(pitest_index_as_string)
        ret = parser.find_alive_mutations(class_name)

        return ret


    def _construct_condensed_mutation_report(self, overview: namedtuple, alive_mutants: list):
        alive_mutants = '\n'.join([f'{status}: {description}' for status, description in alive_mutants])

        report = '\n'.join([
            "Mutation report:",
            f"Coverage: {overview.code_coverage_percent}%, lines covered: {overview.code_coverage_legend}",
            f"Mutants: {overview.mutation_score_percent}%, mutants killed: {overview.mutation_score_legend}",
            "Mutators:",
            alive_mutants
        ])

        self.printer.print_with_color(report, "yellow")
        return report


    def extract_data(self, class_name):
        overview_tuple = self._extract_overview_coverage(class_name)

        # The mutation testing was successful, but failed to find the class or report.
        if overview_tuple is None:
            return (None, None)

        living_mutants = self._extract_living_mutants(class_name)
        report = self._construct_condensed_mutation_report(overview_tuple, living_mutants)

        return overview_tuple, report
    
