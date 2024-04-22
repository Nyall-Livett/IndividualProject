import csv
import os

"""
This class holds the results for a single iteration the process
"""

class Result:

    def __init__(self, project_name, class_name) -> None:
        self.project_name = project_name
        self.class_name = class_name
        self.values = []

    
