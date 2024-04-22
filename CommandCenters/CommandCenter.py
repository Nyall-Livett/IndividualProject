from CommandCenters.BuildSystemEnum import BuildSystem
from CommandCenters.GradleCommandCenter import GradleCommandCenter
from CommandCenters.MavenCommandCenter import MavenCommandCenter
import os
class CommandCenter():

    def __init__(self, build_system) -> None:
        self.build_system = build_system

    def get_command_object(self):
        if self.build_system == BuildSystem.GRADLE:
            return GradleCommandCenter()
        if self.build_system == BuildSystem.MAVEN:
            return MavenCommandCenter()