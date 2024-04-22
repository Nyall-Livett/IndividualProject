import re

"""
This class removes JavaDoc from files
"""

class FileSanitiser:
    """
    Remove leading javadoc from the string content
    """
    def remove_leading_javadoc(self, content):
        return re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
