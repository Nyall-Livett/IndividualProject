import re 
import shutil
import os
from Helper.TerminalPrinter import TerminalPrinter

"""
This class handles the reading and the writing of the files in the projects
"""

class FileIO():

    def __init__(self) -> None:
        self.printer = TerminalPrinter()

    
    def read_file_as_string(self, file_path):
        """
        Read file and return as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except:
            return None


    def write_file_from_string(self, file_path, test_content: str):
        """
        Write to file from a String
        """
        with open(file_path, 'w') as test_file:
            test_file.writelines(test_content)
        return file_path

    def copy_file(self, file_path, new_path):
        """
        Copy file at file_path to the new path new_path
        """
        self.printer.print_with_color("Copy Evosuite file to package", "yellow")
        return shutil.copy(str(file_path), str(new_path))


    def remove_from_file(self, file_path, to_remove):
        """
        Remove specific lines or patterns from a file.
        """
        # Read the original content of the file
        original_content = self.read_file_as_string(file_path)
        if original_content is None:
            print(f"Failed to read {file_path}")
            return

        # Remove the annotations
        modified_content = original_content
        for pattern in to_remove:
            modified_content = re.sub(pattern, '', modified_content, flags=re.DOTALL)

        # Write the modified content back to the file
        self.write_file_from_string(file_path, modified_content)
        
    def is_file_present(self, path):
        if os.path.exists(path):
            return True
        return None
    
    def find_file(self, root_folder, filename):
        for root, dirs, files in os.walk(root_folder):
            if filename in files:
                return os.path.join(root, filename)
        return None
    
    def update_package_in_file(self, test_path, desired_package):
        """
        Update the package name in the Java class file if it doesn't match the desired package.
        """
        # Read the original content of the file
        original_content = self.read_file_as_string(test_path)
        if original_content is None:
            print(f"Failed to read {test_path}")
            return

        # Extract the existing package name from the file
        package_pattern = r'package\s+([\w.]+);'
        match = re.search(package_pattern, original_content)

        if match:
            existing_package = match.group(1)
            if existing_package != desired_package:
                # Replace the existing package name with the desired package name
                modified_content = re.sub(package_pattern, f'package {desired_package};', original_content)
                # Write the modified content back to the file
                self.printer.print_with_color("Updated package name in Evosuite test suite", "yellow")
                self.write_file_from_string(test_path, modified_content)
        else:
            print(f"No package declaration found in {test_path}")


    def add_import_in_file(self, file_path, import_statement):
        """
        Add an import statement to a Java file while keeping it with the other imports.
        """
        # Read the original content of the file
        original_content = self.read_file_as_string(file_path)
        if original_content is None:
            print(f"Failed to read {file_path}")
            return

        # Find the position of the last import statement
        import_pattern = r'^import\s+.*;\s*$'
        import_statements = re.findall(import_pattern, original_content, flags=re.MULTILINE)

        if import_statements:
            last_import_index = original_content.rfind(import_statements[-1]) + len(import_statements[-1])
            # Insert the new import statement after the last import statement
            modified_content = original_content[:last_import_index] + "\n" + import_statement + original_content[last_import_index:]
        else:
            # If no import statements found, insert the new import statement after the package declaration
            package_pattern = r'^package\s+.*;\s*$'
            package_statement = re.search(package_pattern, original_content, flags=re.MULTILINE)

            if package_statement:
                package_index = package_statement.end()
                modified_content = original_content[:package_index] + "\n\n" + import_statement + original_content[package_index:]
            else:
                # If no package declaration found, insert the new import statement at the beginning of the file
                modified_content = import_statement + "\n" + original_content

        # Write the modified content back to the file
        self.write_file_from_string(file_path, modified_content)