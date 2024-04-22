from CommandCenters.ICommandCenter import ICommandCenter
from abc import abstractmethod, ABC
import subprocess

"""
This class should be overridden by the concrete build tool command centers.
"""

class BuildToolCommandCenter(ICommandCenter):

    def __init__(self, project_name):
        super().__init__(project_name)

    @abstractmethod
    def build_project(self, module_dir):
        pass

    @abstractmethod
    def run_test(module_dir, qualified_test_name):
        pass
    
    @abstractmethod
    def run_mutation_test(module_dir, qualified_test_name):
        pass

    def run_command(self, command: list, module_dir, timeout=150):
        """
        Runs the command that has been passed using updated env
        """
        print(f"Running {command} from {module_dir}")

        try:
            result = subprocess.run(command, env=self.os_environment, cwd=f"{module_dir}/", capture_output=True, text=True, timeout=timeout)
        except: 
            self.printer.print_with_color("Subprocess timed out or an exception has occured", "red")
            return None
        return result
    