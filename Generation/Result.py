import csv
import os

class Result:

    def __init__(self, project_name, class_name) -> None:
        self.project_name = project_name
        self.class_name = class_name
        self.values = []

    
