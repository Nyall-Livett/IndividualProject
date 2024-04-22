import os
from pathlib import Path
from openai import OpenAI
from Config import Config
from Helper.TerminalPrinter import TerminalPrinter

class OpenAIUploader:

    OUTPUT_PATH = "training_data.jsonl"

    def __init__(self):
        self.printer = TerminalPrinter()

        self.client = OpenAI(api_key=Config.get_key())
        self.file_path = Path(os.getcwd(), self.OUTPUT_PATH)

    def upload_file(self):
        """
        Upload training data file to openai ready to be used in training a GPT model 
        """
        try:
            upload_response = self.client.files.create(
                file=open(self.file_path, "rb"),
                purpose="fine-tune")
            
            self.printer.print_with_color("Upload Response:", "green")
            self.printer.print_with_color(upload_response, "yellow")
            self.printer.print_with_color("Upload ID:" + upload_response.id, "yellow")
        except Exception as e:
            print("An error occurred during file upload:", e)

        return upload_response.id

    def train_model(self, file_id):
        """
        Train the model ready to used in the project
        """
        self.client.fine_tuning.jobs.create(
            training_file=file_id, 
            model="gpt-3.5-turbo-1106")
        
        self.printer.pretty_print("Model training started")
        
