import re
import subprocess
from util.log import configure_logger
from util.util import find_notebooks_recursive

logger = configure_logger('github-data_logger', 'logging_file.log')


def remove_lines(folder_path: str) -> None:
    """
    Removes lines from a Python file that start with the regular expressions !, @, %, $, install, pip, conda,
    and converts the resulting code to Python 3 syntax using the 2to3 library.

    Args:
        folder_path (str): The path to the folder containing the Python files to modify.

    Returns:
        None
    """
    # Define the regular expressions to be removed
    regex_list = ['^=!', '^#', '^<>', '^=$', r'^\.', '^!', '^@', '^%', '^\$', '^install', '^pip', '^conda']
    regex = '|'.join(regex_list)

    pattern = '.py'
    python_paths = find_notebooks_recursive(folder_path, pattern)
    for filepath in python_paths:
        # Read the file contents
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                contents = file.read()

            # Remove the lines matching the regular expressions
            contents = '\n'.join(line for line in contents.split('\n') if not re.match(regex, line))
            print(contents)

            # Write the modified contents back to the same file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(contents)
        except Exception as e:
            print(f"Error on {filepath} : {e}")
        # Convert the code to Python 3 syntax using the 2to3 command-line tool
        # result = subprocess.run(['2to3', '-w', filepath], capture_output=True, text=True)
        # logger.info(result.stdout)
