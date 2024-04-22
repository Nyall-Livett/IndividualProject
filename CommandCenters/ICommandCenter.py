from abc import ABC
import subprocess
import os
from Helper.TerminalPrinter import TerminalPrinter

class ICommandCenter(ABC):

    def __init__(self, project_name):
        self.printer = TerminalPrinter()
        self.project_name = project_name


    def configure_environment(self):
        """
        Configure the os enviroment with the correct Java version for the current 
        project
        """
        self.os_environment = os.environ.copy()
        print(f"Setting {self.project_name} JDK to {self.project_java_versions.get(self.project_name)}")
        jdk_path = self.__get_jdk_path_for_project(self.project_name)

        if jdk_path is None:
            print(f"Error cannot process project {self.project_name}")
            return
        
        self.os_environment["JAVA_HOME"] = jdk_path
        self.os_environment["PATH"] = jdk_path + "/bin:" + self.os_environment["PATH"]

    def __get_jdk_path_for_project(self, project: str):
        """
        Returns the path to Java version used by the project. 
        """
        version = self.project_java_versions.get(project, None)

        if version is None:
            print("Error project java version not included")
            return None

        command = ['/usr/libexec/java_home', '-v',  f'{version}']
        result = self.run_command(command, os.getcwd())

        if result.returncode == 0:
            return result.stdout.strip()

        print(f"Error finding Java home for version {version}: {result.stderr}")
        return None


    def run_command(self, command: list, module_dir, timeout=150):
        """
        Runs the command that has been passed using updated env
        """
       
        print(f"Running {command} from {module_dir}")
        # self.configure_environment()
        try:
            result = subprocess.run(command, env=self.os_environment, cwd=f"{module_dir}/", capture_output=True, text=True, timeout=timeout)
        except: 
            self.printer.print_with_color("Subprocess timed out", "red")
            return None
        return result
    
    
    