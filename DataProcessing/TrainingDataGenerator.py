import json
import os
import shutil
from pathlib import Path
from Helper.TerminalPrinter import TerminalPrinter

class TrainingDataGenerator:
    SYSTEM : str = "Welcome to the Automated Java Testing Service! Please submit your Java code below"
    USER : str = "Given the following Java code, please generate comprehensive unit tests using JUnit. Ensure the tests cover all functions adequately, including edge cases and typical use cases. Here is the Java code: %Class%"
    ASSISTANT : str = "%Tests%"
    OUTPUT_PATH = "training_data.jsonl"
    
    def __init__(self):
        self.printer = TerminalPrinter()
        self.processed_files_dir = os.path.join(os.getcwd(), "processed_files")
        self.formatted_entries = []
    

    def process_project_training_data(self, project_training_dir):
            for subdir, _, files in os.walk(project_training_dir):
                for file in files:
                    if file.startswith("."):
                        continue
                    if not file.endswith("Test.java"):
                        class_file_path = os.path.join(subdir, file)
                        test_file_path = os.path.join(subdir, file.replace(".java", "Test.java"))

                        with open(class_file_path, 'r', encoding='utf-8') as class_file:
                            class_content = class_file.read()
                        
                        if class_content is None or class_content == "":
                            continue

                        with open(test_file_path, 'r', encoding='utf-8') as test_file:
                            test_content = test_file.read()
                        
                        if test_content is None or test_content == "":
                            continue
                        
                        entry = {
                            "messages": [
                                {"role": "system", "content": self.SYSTEM},
                                {"role": "user", "content": self.USER.replace("%Class%", class_content)},
                                {"role": "assistant", "content": self.ASSISTANT.replace("%Tests%", test_content)}
                            ]
                        }
                        
                        self.formatted_entries.append(entry)
        


    def generate(self):
        for project_dir in os.listdir(self.processed_files_dir):
            project_path = Path(self.processed_files_dir, project_dir, "training_data")
            if project_path.is_dir():
                self.process_project_training_data(project_path)
        
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as output_file:
            for entry in self.formatted_entries:
                json_line = json.dumps(entry, ensure_ascii=False) + '\n'
                output_file.write(json_line)
        print()
        self.printer.print_with_color(f"Training data has been generated and saved to {self.OUTPUT_PATH}", "green")
        print()

generator = TrainingDataGenerator()
generator.generate()