import os
import csv
# from Handler.HumanHandler import HumanHandler
# from Handler.LLM1Handler import LLM1Handler
# from Handler.EvosuiteHandler import EvosuiteHandler

class CsvWriter:

    # handler_classes = [
    #         HumanHandler,
    #         EvosuiteHandler,
    #         LLM1Handler,
    #     ]
    
    def __init__(self, file_name, handlers):
        self.file_name = file_name
        self.handler_classes = handlers
        self.create_csv_file()

    def get_headers(self):
        """
        Include the default headers for the Project name and class
        """
        csv_headers: list = ["PROJECT_name", "CLASS_name"]
        for handler_class in self.handler_classes:
            csv_headers.extend(handler_class.get_csv_headers())
        return csv_headers    

    def create_csv_file(self):
        """
        Create the CSV file and write the header row if it doesnt already exist
        """
        # File doesnt exist, create it and write the headers as the first line.
        if not os.path.exists(self.file_name):

            headers = self.get_headers()
            
            with open(self.file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
            print(f"Created new CSV file with headers at: {self.file_name}")
        
        else:
            print(f"CSV file already exists at: {self.file_name}")

    def write_row(self, result):
        """
        Write results to the csv file
        """
        values = [result.project_name, result.class_name]
        values.extend(result.values)

        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)

        values = []