from bs4 import BeautifulSoup
from collections import namedtuple

"""
This class handles the parsing of the HTML to extract data about mutations
"""

class HTMLParser():

    COVERAGE_METRICS = namedtuple(
        'coverage_metrics', [
            'code_coverage_percent', 'code_coverage_legend',
            'mutation_score_percent', 'mutation_score_legend',
            'test_strength_percent', 'test_strength_legend'
    ])
    
    def __init__(self, string, result_statistics_obj):
        self.soup = BeautifulSoup(string, 'lxml')
        self.result_statistics_obj = result_statistics_obj


    def extract_mutation_scores(self, class_name):
        anchor = self.soup.find('a', string=class_name)
        
        # No mutation data for current test
        if anchor is None: 
            print(f"Error no mutation coverage for {class_name}")
            self.result_statistics_obj.initial_mutation_test_runs = False
            return None
        
        # Initialize lists to store the percentages and legends
        coverage_percentages = []
        coverage_legends = []

        # Extract coverage percentages
        for div in anchor.find_all_next('div', class_='coverage_percentage', limit=3):
            coverage_percentages.append(int(div.get_text().strip().strip('%')))
        
        # Extract coverage legends
        for div in anchor.find_all_next('div', class_='coverage_legend', limit=3):
            coverage_legends.append(div.get_text().strip())

        # Zip the percentages and legends together and flatten the list
        metrics_values = [val for pair in zip(coverage_percentages, coverage_legends) for val in pair]

        # Create and return the COVERAGE_METRICS namedtuple with extracted data
        metrics = self.COVERAGE_METRICS(*metrics_values)
        return metrics