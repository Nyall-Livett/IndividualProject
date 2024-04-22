import re

class FileSanitiser:
    """
    Remove leading javadoc from the string content
    """
    def remove_leading_javadoc(self, content):
        return re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
