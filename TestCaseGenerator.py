import os
from pathlib import Path
from Generation.Result import Result
from File.FileSanitiser import FileSanitiser
from File.FileIO import FileIO
from Handler.EvosuiteHandler import EvosuiteHandler
from Handler.HumanHandler import HumanHandler
from Handler.LLM1Handler import LLM1Handler
from Handler.LLM2Handler import LLM2Handler
from Handler.LLM3Handler import LLM3Handler
from Handler.LLM4Handler import LLM4Handler
from Generation.TestRunner import TestRunner
from Helper.TerminalPrinter import TerminalPrinter
from File.CsvWriter import CsvWriter
from Helper.PathHelper import PathHelper

"""
This class is the entry point for the test generation
"""

class TestCaseGenerator:

    PROCESSED_FILES_DIR_NAME: str = "processed_files"
    TEST_DATA_DIR_NAME: str = "test_data"
    PROJECTS_FOR_DATA : str = "projects-used-for-data"
    FILE_NAME = "results.csv"
    
    # Not included in the testing phase.
    not_included = ["questdb", "javaparser", "Java"]

    # Add handler here to include them in the evaluation
    handler_classes = [
        HumanHandler,
        EvosuiteHandler,
        LLM1Handler,
        LLM2Handler,
        LLM3Handler,
        LLM4Handler
    ]

    file_io = FileIO()
    file_sanatiser = FileSanitiser()
    printer = TerminalPrinter()
    csv_writer = CsvWriter(FILE_NAME, handler_classes)
    skip_until = False
    
    def __init__(self) -> None:
        self.path_helper = PathHelper()
        self.current_working_dir = os.getcwd() 
        self.processed_files_dir = os.path.join(self.current_working_dir, self.PROCESSED_FILES_DIR_NAME)
        self.projects_for_data_dir = os.path.join(self.current_working_dir, self.PROJECTS_FOR_DATA)

    def generate_for_all(self):
        """
        Generate test cases for all projects in the processed_files_dir.
        Iterates over every obj in the processed_files_dir directory, If the obj is a dir
        then process it for test generation. 
        """
        for project_dir in Path(self.processed_files_dir).iterdir():
            if project_dir.is_dir() and project_dir.name not in self.not_included: #and project_dir.name == "mybatis-3":
                test_data_dir = project_dir / self.TEST_DATA_DIR_NAME
                if test_data_dir.exists():
                    self.generate_for_one(project_dir.name, test_data_dir)
                    print(f"Processed project: {project_dir.name}")


    def generate_for_one(self, project_name, processed_project_path: Path):
        """
        Generate test cases for one project by iterating through the test_data directory
        for the given project, extracting the content from the Test class and pass them to an LLM to 
        produce the test class.
        """

        self.printer.clear_terminal()

        skip = ["RedisPriorityScheduler.java", "WebDriverPool.java",
                "WebDriverPoolTest.java"]

        for root, _, files in os.walk(processed_project_path):
            for file in files:
                
                if file in skip:
                    continue
                
                # This is used if you want to fast track to a particular class in the process
                # if file == "UdfFunc.java":
                #     self.skip_until = True

                # if not self.skip_until:
                #     continue


                # Create TestRunner and Result object
                if not file.endswith("Test.java") and file.endswith(".java"): # get the class file and ignore the test file
                    test_runner: TestRunner = TestRunner(project_name)
                    result = Result(project_name, file)
                    file_string = self.file_io.read_file_as_string(Path(root, file))
                    
                    if file_string is None:
                        continue

                    self.start_process(file, project_name, file_string, result, test_runner)


    def start_process(self, class_name, project_name,  class_as_string, result: Result, test_runner: TestRunner):
        """
        Initiates the process involved in generation and evalution.
        """
        original_test_file_path = None
        original_test_file = None
        try:
            self.printer.pretty_print(class_name)
            original_test_file_path = self.find_test_file(class_name, project_name)

            if original_test_file_path is None:
                return
            
            original_test_file = self.file_io.read_file_as_string(original_test_file_path)

            original_class_file_path = self.find_class_file(class_name, project_name, original_test_file_path)
            
            if original_class_file_path is None:
                return


            handlers: list = [
                HumanHandler(result, test_runner, class_name, original_test_file_path, original_class_file_path),
                EvosuiteHandler(test_runner, original_test_file_path, original_class_file_path, class_name, result),
                LLM1Handler(result, test_runner, class_as_string, class_name, original_test_file_path, original_class_file_path, original_test_file),
                LLM2Handler(result, test_runner, class_as_string, class_name, original_test_file_path, original_class_file_path, original_test_file),
                LLM3Handler(result, test_runner, class_as_string, class_name, original_test_file_path, original_class_file_path, original_test_file),
                LLM4Handler(result, test_runner, class_as_string, class_name, original_test_file_path, original_class_file_path, original_test_file)
            ]

            # Execute the handlers
            for handler in handlers:
                handler.execute()

        except KeyboardInterrupt:
            self.printer.print_with_color("Keyboard interrupt", "red")
            raise
    
        except:
            self.printer.print_with_color("Something has gone wrong", "red")
            return
        
        finally:
            # Put back original test file before the generation happened
            if not original_test_file is None:  
                self.file_io.write_file_from_string(original_test_file_path, original_test_file)
            self.csv_writer.write_row(result)
            


    def find_test_file(self, class_name, project_name):
        """
        Finds the parent folder of the test file used in the generating the new tests.
        Returns the path the to folder.
        """
        test_name = f"{class_name[:-5]}Test.java"
        project_path = Path(self.projects_for_data_dir, project_name)
        
        for dirpath, _, filenames in os.walk(project_path):
            if test_name in filenames:  
                return Path(dirpath, test_name)
        return None 
    
    def find_class_file(self, class_name, project_name, test_path):
        """
        Trys to locate the Java class file associated with the test by walking the project matching
        files with the class name.
        Excludes the files in target folder as theses are the .class files. 
        Can return None if a definite match cannot be found. 
        """
        project_path = Path(self.projects_for_data_dir, project_name)
        potential_paths = []

        # Walk through the project directory
        for dirpath, _, filenames in os.walk(project_path):
            if 'target' in dirpath.split(os.sep):
                continue  # Skip directories containing 'target'
            
            if class_name in filenames:
                potential_paths.append(Path(dirpath, class_name))
        
        # No matching class file found
        if not potential_paths:
            return None
        
        # If there is one potential path than its a match
        if len(potential_paths) == 1:
            return potential_paths[0]

        module_dir = self.path_helper._determine_module_path(test_path)
        class_module_dirs = [self.path_helper._determine_module_path(path.parent) for path in potential_paths]
        matching_paths = [path for path, class_module_dir in zip(potential_paths, class_module_dirs) if module_dir == class_module_dir]
        
        # Handle the result based on the number of matching paths
        if len(matching_paths) == 1:
            return matching_paths[0]
       
        elif not matching_paths:
            print("No class file found in the same module as the test.")
            return None
        else:
            print("Multiple potential class files found")
            return None


testCase= TestCaseGenerator()
testCase.generate_for_all()
