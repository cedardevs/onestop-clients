import os

# This function that takes a source file path and a target relative path and creates an absolute path to the target file
def abspath_from_relative(path_from, rel_path_to):
    return os.path.abspath(os.path.join(os.path.dirname(path_from), rel_path_to))
