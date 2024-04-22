from CommandCenters.BuildSystemEnum import BuildSystem
from CommandCenters.MavenCommandCenter import MavenCommandCenter
class CommandCenterManager():

    def __init__(self, build_system) -> None:
        self.build_system = build_system

    def get_command_object(self, project_name):
        """
        Allow for different buils systems such as Gradle
        """
        if self.build_system == BuildSystem.MAVEN:
            return MavenCommandCenter(project_name)