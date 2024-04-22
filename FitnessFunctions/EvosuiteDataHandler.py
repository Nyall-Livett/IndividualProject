import re

class EvosuiteDataHandler():
   
    def extract_data(self, evosuite_output):
        """
        Extracts coverage and mutation score data from the given EvoSuite output string.

        Parameters:
        evosuite_output (str): The output string from EvoSuite.

        Returns:
        tuple: Coverage and mutation score extracted from the output.
        """
        coverage_pattern = r"\* Resulting test suite's coverage: (\d+)%"
        mutation_score_pattern = r"\* Resulting test suite's mutation score: (\d+)%"
        coverage = None
        mutation_score = None

        coverage_match = re.search(coverage_pattern, evosuite_output)
        if coverage_match:
            coverage = coverage_match.group(1)

        mutation_score_match = re.search(mutation_score_pattern, evosuite_output)
        if mutation_score_match:
            mutation_score = mutation_score_match.group(1)

        return coverage, mutation_score