from CommandCenters.CommandCenterManager import CommandCenterManager
from CommandCenters.BuildSystemEnum import BuildSystem
from FitnessFunctions.MutationDataHandler import MutationDataHandler
from CommandCenters.ShellCommandCenter import ShellCommandCenter
import os
from Helper.PathHelper import PathHelper
from File.FileIO import FileIO

"""
This class is responsible for running the generated tests and also running the mutation tests
"""

class TestRunner():
    
    BUILD_SYSTEM: BuildSystem = None
    PROJECTS_FOR_DATA : str = "projects-used-for-data"

    def __init__(self, project_name) -> None:
        """
        Create the Path object for the project to run tests on.
        """
        self.current_working_dir = os.getcwd()
        self.path_helper = PathHelper()
        self.actual_project_path = os.path.join(self.current_working_dir, self.PROJECTS_FOR_DATA, project_name)
        self.__configure(self.actual_project_path, project_name)
        self.file_handler : FileIO = FileIO()


    def __configure(self, actual_project_path, project_name):
        """
        Configure properties from the project which will impact the commands to run the tests.
        """
        self.BUILD_SYSTEM = self.__determine_build_system(actual_project_path)
        self.shell_runner = ShellCommandCenter(project_name)
        self.command_center = CommandCenterManager(self.BUILD_SYSTEM).get_command_object(project_name)
        self.command_center.configure_environment()
        self.shell_runner.configure_environment()
        
        
    def __determine_build_system(self, project_path):
        """
        Determine what the build system of the project is by creating a path with build.gradle
        or pom.xml and seeing if it the path exists in the project.
        """
        if os.path.exists(os.path.join(project_path, 'build.gradle')):
            return BuildSystem.GRADLE
        if os.path.exists(os.path.join(project_path, 'pom.xml')):
            return BuildSystem.MAVEN
        

    def run_evosuite(self, test_path, class_path):
        """
        Run evosuite test generation
        """
        qualified_class_name = self.path_helper._determine_fully_qualified_class_name(class_path)
        module_dir = self.path_helper._determine_module_path(test_path)
        root_dir = self.path_helper._determine_root_directory_path(test_path)
        
        return self.shell_runner.run_evosuite_command(root_dir, module_dir, qualified_class_name)


    def run_unit_test(self, test_path):
        """
        Run unit test using module directory and test name
        """
        module_dir = self.path_helper._determine_module_path(test_path)
        qualified_test_name = self.path_helper._determine_fully_qualified_test_name(test_path)
        return self.command_center.run_test(module_dir, qualified_test_name)


    def run_mutation_test(self, test_path, class_name, result_statistics_obj, class_path):
        """
        Run mutation testing software.
        """
        module_dir = self.path_helper._determine_module_path(test_path)
        class_module_dirs = self.path_helper._determine_module_path(class_path)
        qualified_test_name = self.path_helper._determine_fully_qualified_test_name(test_path)
        package_name = self.path_helper._determine_full_package_name(class_path)
        
        mutation_handler = MutationDataHandler(self.BUILD_SYSTEM, class_module_dirs, package_name, result_statistics_obj)
        mutation_handler.delete_folder()

        # Ret could be None, that means the subprocess either timed out and caused an Exception
        ret = self.command_center.run_mutation_test(module_dir, qualified_test_name)
        
        # Error when running subprocess
        if ret is None:
            return False, None

        return mutation_handler.extract_data(class_name)
