import subprocess
from pathlib import Path
from CommandCenters.ICommandCenter import ICommandCenter

class ShellCommandCenter(ICommandCenter):

    project_java_versions : dict = {
        "mybatis-3": 11,
        "webmagic": 11,
        "Java": 17,
        "jkube": 11,
        "java-design-patterns": 11,
        "javaparser": 11,
        "dolphinscheduler": 11,
        "questdb": 1.8,
        "Hikari": 11,
        "IndividualProject-sample": 11
    }

    full_classpath_projects: list = ["dolphinscheduler", "jkube"]

    os_environment = None

    def __init__(self, project_name):
        super().__init__(project_name)

    def run_evosuite_command(self, root_dir, module_dir, qualified_class_name):
        """
        Runs shell command for Evosuite
        """
        if self.project_java_versions.get(self.project_name) > 11:
            self.printer.print_with_color(f"Project {self.project_name} does not support Evosuite", "white")
            return False
        
        if self.project_name in self.full_classpath_projects:
            classpath_file = Path(module_dir, "classpath.txt")

            try:
                with open(classpath_file, 'r') as file:
                    classpath_content = file.read().strip()
            except IOError:
                self.printer.print_with_color("Failed to read classpath file", "red")
                return False            
            classpath = f"{classpath_content}:{module_dir}/target/classes"
        else:
            classpath = f"{module_dir}/target/classes"    


        print("Running shell command for Evosuite")
        command = [
            'java',
            '-jar', f'{root_dir}/evosuite-1.2.0.jar',
            '-class', qualified_class_name,
            '-projectCP', classpath,
            "-Duse_separate_classloader=false",
            "-Dsearch_budget=20",
            "-Dtest_format=JUNIT5"
        ]

        # self.configure_environment()
        ret = self.run_command(command,  module_dir)
        self.printer.print_with_color("Evosuite has been executed", "green")
        return ret

    def run_command(self, command: list, module_dir):
        """
        Runs the command that has been passed using updated env
        """
        result = subprocess.run(command, env=self.os_environment, cwd=module_dir, capture_output=True, text=True)
        return result