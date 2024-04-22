from pathlib import Path

class PathHelper:

    def _determine_module_path(self, test_path):
        """
        Determine the module path used as the cwd when calling the tests
        """
        return str(test_path).rsplit('/src/', 1)[0]

    def _determine_class_module_path(self, test_paths):
        """
        Determine the module path used as the cwd when calling the tests
        """
        module_paths = []
        for test_path in test_paths:
            module_path = str(test_path).rsplit('/src/', 1)[0]
            module_paths.append(module_path)
        return module_paths


    def _determine_root_directory_path(self, test_path):
        """
        Determine the root directory path from a full test path, assuming it is directly after 'projects-used-for-data'.
        """
        parts = Path(test_path).parts
        # Find the index of 'projects-used-for-data' and take the next part as the root directory
        project_index = parts.index('projects-used-for-data') if 'projects-used-for-data' in parts else -1
        if project_index != -1 and project_index + 1 < len(parts):
            root_dir = Path(*parts[:project_index + 2])
            return str(root_dir)
        return ""

    def _determine_fully_qualified_test_name(self, test_path):
        """
        Determine the qualified name used for calling the tests
        """
        return str(test_path).rsplit('/java/', 1)[1].replace('/', '.').rsplit('.java', 1)[0]


    def _determine_fully_qualified_class_name(self, test_path):
        """
        Determine the qualified name used for calling the tests
        """
        return str(test_path).rsplit('/java/', 1)[1].replace('/', '.').rsplit('.java', 1)[0].replace('Test', '')


    def _determine_full_package_name(self, test_path):
        """
        Determine the qualified name used for calling the tests as a path
        """
        return str(Path(str(test_path).rsplit('/java/', 1)[1]).parent).replace('/', '.')


    def _determine_evosuite_test_paths(self, test_path):
        es_test_folder = Path(self.__determine_module_path(test_path)) / "evosuite-tests"
        es_test_name = self.__determine_fully_qualified_test_name(test_path)

        str_path = str(es_test_folder / es_test_name)[:-4]
        es_test_path = str_path + "_ESTest"
        es_scaffolding_path = str_path + "_ESTest_scaffolding"
        return es_test_path.replace(".", "/") + ".java", es_scaffolding_path.replace(".", "/") + ".java"

    def _determine_evosuite_test_paths(self, path):
        es_test_folder = Path(self._determine_module_path(path)) / "evosuite-tests"
        es_test_name = self._determine_fully_qualified_test_name(path)
        str_path = str(es_test_folder / es_test_name)
        es_test_path = str_path + "_ESTest"
        es_scaffolding_path = str_path + "_ESTest_scaffolding"
        return es_test_path.replace(".", "/") + ".java", es_scaffolding_path.replace(".", "/") + ".java"

