from enum import Enum, auto

"""
Enum for build tools
"""

class BuildSystem(Enum):
        GRADLE = auto(),
        MAVEN = auto(),
        MULTIBUILD = auto()

