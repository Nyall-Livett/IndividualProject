import os
from CommandCenters.BuildToolCommandCenter import BuildToolCommandCenter

class MavenCommandCenter(BuildToolCommandCenter):
    os_environment = None

    ERROR_CODE: int = 1

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
        "Nyall-Livett-IndividualProject-sample": 11
    }

    def __init__(self, project_name):
        super().__init__(project_name)

    def build_project(self, module_dir):
        """
        Creates the command for compiling the project and then passes the command 
        to the runner to be exectuted
        """
        print(f"Building {os.path.basename(module_dir)}")
        command = ['mvn', 'compile']
        ret =  self.run_command(command, module_dir)
        self.printer.print_with_color("Completed Building project", "green")
        return ret


    def run_test(self, module_dir, qualified_test_name):
        """
        Creates the command for running a single test and then passes the command 
        to the runner to be exectuted
        """
        print(f"Running test {qualified_test_name}")

        command = [
            'mvn', 'test', '-Dtest=' + qualified_test_name,
            '-Dcheckstyle.skip=true',
            '-Dlicense.skip=true',
            '-Dmaven.javadoc.skip=true',
            '-Denforcer.skip=true',
            '-Dgit-commit-id.skip=true',
            '-Djacoco.skip=true',
            '-Dformatter.skip=true',
            '-Dimpsort.skip=true',
            '-Drewrite.skip=true'
        ]
        # self.configure_environment()
        ret = self.run_command(command,  module_dir)
        self.printer.print_with_color("Unit test has been executed", "green")
        
        # Could be None if subprocess timed out or an Exception     
        if ret is None:
            return None

        if ret.returncode == self.ERROR_CODE:
            self.printer.print_with_color("The unit tests produced failures or errors", "red")
        return ret
    

    def run_mutation_test(self, module_dir, qualified_test_name):
        """
        Runs the mutation testing software
        """
        print(f"Running mutation test for {qualified_test_name}")
        command = ['mvn', 'org.pitest:pitest-maven:mutationCoverage',
                '-DtargetTests=' + qualified_test_name, 
                '-DoutputFormats=HTML,XML',
                '-Dcheckstyle.skip=true',
                '-Dlicense.skip=true',
                '-Dmaven.javadoc.skip=true',
                '-Denforcer.skip=true',
                '-Dgit-commit-id.skip=true',
                '-Djacoco.skip=true',
                '-Dformatter.skip=true',
                '-Dimpsort.skip=true',
                '-Drewrite.skip=true',
                ]
        
        # Ret could be None due to timeout or Exception.
        ret = self.run_command(command,  module_dir)
        self.printer.print_with_color("Mutation testing has been executed", "green")
        return ret
    