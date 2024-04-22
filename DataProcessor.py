import os
from File.FileSanitiser import FileSanitiser
from File.FileIO import FileIO
from LLM.OpenAiHelper import OpenAiHelper
from Helper.TerminalPrinter import TerminalPrinter
from pathlib import Path
from DataProcessing.DataSplitter import DataSplitter
from DataProcessing.TrainingDataGenerator import TrainingDataGenerator
from LLM.OpenAIUploader import OpenAIUploader
from DataProcessing.TrainingDataValidator import TrainingDataValidator

class DataProcesser:
    
    # Name of directory where the projects used for data collection are
    PROJECTS_FOR_DATA : str = "projects-used-for-data"
    PROCESSED_FILES_DIR_NAME : str = "processed_files"
    MODEL : str = 'gpt-3.5-turbo-1106'

    def __init__(self) -> None:
        self.printer = TerminalPrinter()
        self.current_working_dir = os.getcwd() 
        self.processed_files_dir = os.path.join(self.current_working_dir, self.PROCESSED_FILES_DIR_NAME)
        self.projects_for_data_dir = os.path.join(self.current_working_dir, self.PROJECTS_FOR_DATA)


    def process_projects(self):
        dirs = self.get_subdirectory_paths()

        for dir in dirs:
            # if dir != "/Users/nyalllivett/Desktop/LLMTestGeneration/projects-used-for-data/dolphinscheduler":
            #     continue
            test_files, non_test_files = self.get_file_pairs(dir)
            self.process_pairs(self.extract_project_name(dir), test_files, non_test_files)

        splitter = DataSplitter()

        splitter.split_project_folders()

        generate_response = input("Do you want to generate the training data? : ").strip().lower()
        
        if generate_response == 'yes' or generate_response == 'y':
            training_data_generator = TrainingDataGenerator()
            training_data_generator.generate()
        else:
            return

        validator = TrainingDataValidator("training_data.jsonl")
        validator.validate()


        upload_response = input("Do you want to upload the training data? : ").strip().lower()
        
        if upload_response == 'yes' or upload_response == 'y':

            openai_file_uploader = OpenAIUploader()
            file_id = openai_file_uploader.upload_file()
            train_response = input("Do you want to train the model on the test file? : ").strip().lower()
            if train_response == 'yes' or train_response == 'y':
                openai_file_uploader.train_model(file_id)
                

    """
    Returns all subdirectories within the PROJECTS_FOR_DATA directory - these subdirectories are the 
    projects that are going to be used to extract classes and test classes from.
    The iterable exclude_dirs include directory names that shouldnt be included in the class extraction
    """
    def get_subdirectory_paths(self, exclude_dirs=[]) -> list:
        self.printer.pretty_print("Finding subdirectories")
 
        subdirectories = [os.path.join(self.projects_for_data_dir, d) for d in os.listdir(self.projects_for_data_dir) 
            if os.path.isdir(os.path.join(self.projects_for_data_dir, d)) and d not in exclude_dirs]

        self.printer.print_with_color(f"\n{len(subdirectories)} subdirectories found", "green")
    
        for subdir in subdirectories:
                self.printer.print_with_color(self.extract_project_name(subdir), "yellow")
        
        return subdirectories
    

    """
    Takes a subdirectory (project) to walk through and find classes and test classes that follow these rules
    Example.java
    ExampleTest.java
    and puts them into a dictionary with the key as the file name and the value as the file path
    """
    def get_file_pairs(self, subdirectory):
        test_files = {}
        non_test_files = {}

        for root, dirs, files in os.walk(subdirectory):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith('Test.java'):
                    test_files[file[:-9]] = full_path
                elif file.endswith('.java'):
                    non_test_files[file[:-5]] = full_path
        return test_files, non_test_files


    """
    Walks through the dictionary and checks the whether the key is present in the dictionary which has 
    the java files, if there is a match that means there is a class and its test file which can be used
    in training.
    """
    def process_pairs(self, project_name, test_file_dictionary, non_test_file_dictionary):
        pairs_found = 0
        pairs_passed = 0
        pairs_failed = 0

        file_reader = FileIO()
        file_sanitiser = FileSanitiser()
        open_ai_formatter = OpenAiHelper(self.MODEL)

        for test_file_name, test_file_path in test_file_dictionary.items():
            if test_file_name in non_test_file_dictionary:

                # There is a Class which corresponds to the Test class so this is a pair i can use for training
                pairs_found += 1
                non_test_file_path = non_test_file_dictionary[test_file_name]

                test_content: str = file_reader.read_file_as_string(test_file_path)
                non_test_content: str = file_reader.read_file_as_string(non_test_file_path)

                sanitised_test_content: str = file_sanitiser.remove_leading_javadoc(test_content)
                sanitised_non_test_content: str = file_sanitiser.remove_leading_javadoc(non_test_content)

                combined_content = sanitised_test_content + "\n" + sanitised_non_test_content

                if open_ai_formatter.is_training_data_overflow(combined_content):
                    pairs_passed += 1
                    processed_project_files = os.path.join(self.processed_files_dir, project_name)
                    self.save_to_directory(processed_project_files, test_file_name, os.path.basename(test_file_path), sanitised_test_content)
                    self.save_to_directory(processed_project_files, test_file_name, os.path.basename(non_test_file_path), sanitised_non_test_content)
                else:
                    pairs_failed += 1
        
        print()
        self.printer.print_with_color(project_name, "yellow")
        self.printer.print_with_color("Test pairs found : " + str(pairs_found), "green")
        self.printer.print_with_color("Test pairs found within token limit : " + str(pairs_passed), "green")
        self.printer.print_with_color("Test pairs found not within token limit : " + str(pairs_failed), "red")

        return pairs_found, pairs_passed, pairs_failed


    """
    Save the Java class and test class inside the processed_files dir, inside another dir relating 
    to the project that the class came from.
    Example:
    processed_files > caffeine > CacheLoader > [CacheLoaderTest.java, CacheLoader.java]
    """
    def save_to_directory(self, processed_project_files, sub_directory, filename, content):
        directory = os.path.join(processed_project_files, sub_directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as file:
            file.write(content)

    def extract_project_name(self, path: Path):
        return os.path.basename(path)



processer = DataProcesser()
processer.process_projects()
