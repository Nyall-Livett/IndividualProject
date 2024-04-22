import os
import shutil
from math import ceil
import random
from Helper.TerminalPrinter import TerminalPrinter

"""
This class splits files into different folders. 
"""

class DataSplitter:

    TRAIN_RATIO: float = 0.7
    PROCESSED_FILES_DIR_NAME : str = "processed_files"

    def __init__(self) -> None:
        self.printer = TerminalPrinter()
        self.current_working_dir = os.getcwd()
        self.processed_files_dir = os.path.join(self.current_working_dir, self.PROCESSED_FILES_DIR_NAME)

    """
    Write comment for this
    """
    def split_project_folders(self):
        
        self.printer.pretty_print("Splitting data")

        # Iterate over each project folder in the processed_files directory
        for project in os.listdir(self.processed_files_dir):
            project_path = os.path.join(self.processed_files_dir, project)
            if os.path.isdir(project_path):
                # Define the paths for the training and test data directories within each project folder
                train_dir = os.path.join(project_path, 'training_data')
                test_dir = os.path.join(project_path, 'test_data')

                # Create the training and test directories if they don't already exist
                if not os.path.exists(train_dir):
                    os.makedirs(train_dir)
                if not os.path.exists(test_dir):
                    os.makedirs(test_dir)

                all_subdirs = [d for d in os.listdir(project_path) 
                               if os.path.isdir(os.path.join(project_path, d)) 
                               and d not in ['training_data', 'test_data']]

                # Get a shuffled list of the subdirectories
                shuffled_subdirs = random.sample(all_subdirs, len(all_subdirs))

                # Calculate number of directories for training based on training ratio (70/30)
                number_of_training_dirs = int(ceil(self.TRAIN_RATIO * len(shuffled_subdirs)))

                # Split the directories
                train_subdirs = shuffled_subdirs[:number_of_training_dirs]
                test_subdirs = shuffled_subdirs[number_of_training_dirs:]

                # Function to move directories
                def move_dirs(subdirs, destination):
                    for subdir in subdirs:
                        src_dir = os.path.join(project_path, subdir)
                        dest_dir = os.path.join(destination, subdir)

                        # If folder already present, remove it. 
                        if os.path.exists(dest_dir):
                            shutil.rmtree(dest_dir)
                        shutil.move(os.path.join(project_path, subdir), destination)

                # Move the directories to their respective new locations
                move_dirs(train_subdirs, train_dir)
                move_dirs(test_subdirs, test_dir)

                print("")
                self.printer.print_with_color(f"Processed {project}:", "green")
                self.printer.print_with_color(f" - Moved {len(train_subdirs)} directories to {os.path.basename(train_dir)}", "yellow")
                self.printer.print_with_color(f" - Moved {len(test_subdirs)} directories to {os.path.basename(test_dir)}", "yellow")
                print("")
