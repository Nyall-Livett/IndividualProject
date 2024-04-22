import subprocess

class GradleCommandCenter():

    def set_jdk(self, project_name, module_dir):
        """
        Sets the correct JDK to be able work with the project.
        This makes use of a custom shell command 'setjdk'
        """
        print(f"Setting {project_name} JDK to {self.project_java_versions(project_name)}")
        command = ['setjdk',f"{self.project_java_versions(project_name)}"]
        self.run_command(command, module_dir)
        v_command = ['java','--version']
        print(f"{self.run_command(v_command, module_dir)}")


    def build_project(self, module_dir):
        """
        Creates the command for building the project and then passes the command 
        to the runner to be exectuted
        """
        command = ['./gradlew', 'build']
        return self.run_command(command, module_dir)


    def run_test(self, module_dir, test_name):
        """
        Creates the command for running a single test and then passes the command 
        to the runner to be exectuted
        """
        command = ['./gradlew', '--tests', test_name]
        return self.run_command(command, module_dir)


    def run_command(self, command: list, module_dir):
        """
        Runs the command that has been passed
        """
        result = subprocess.run(command, cwd=module_dir, capture_output=True, text=True)
        return result







#         # Run the test
# def run_test(project_dir, build_system, test_class_path):
#     module_name, class_name = extract_module_and_class(test_class_path)

#     if build_system == 'gradle':
#         command = ['./gradlew', '--tests', class_name]
#     elif build_system == 'maven':
#         # Specify the module with -pl and the test class with -Dtest
#         command = ['mvn', 'test', '-Dtest=' + class_name]
#     else:
#         raise Exception("no build tool")

#     result = subprocess.run(command, cwd=project_dir, capture_output=True, text=True)
#     return result