import os
import nbformat
from nbconvert.exporters.python import PythonExporter

from util.log import configure_logger
from util.util import find_notebooks_recursive

logger = configure_logger('github-data_logger', 'logging_file.log')


# def convert_notebooks_to_python_recursive(folder_path: str) -> None:
#     """
#     Recursively converts all Jupyter notebooks in a specified folder and its subfolders to Python files,
#     saves the Python files in the same folder, and deletes the original notebook files.
#
#     Args:
#     - folder_path (str): The path to the folder containing the Jupyter notebooks to convert.
#
#     Returns:
#     - None
#     """
#     exporter = PythonExporter()
#     pattern = '.ipynb'
#     notebook_paths = find_notebooks_recursive(folder_path, pattern)
#     logger.info(f"number of notebook {len(notebook_paths)}")
#     for notebook_path in notebook_paths:
#         logger.info(f"Converting {notebook_path}")
#         python_path = os.path.splitext(notebook_path)[0] + '.py'
#         with open(notebook_path, 'r', encoding='utf-8') as nb_file:
#             python_code, _ = exporter.from_file(nb_file)
#             with open(python_path, 'w', encoding='utf-8') as py_file:
#                 py_file.write(python_code)
#         os.remove(notebook_path)

def convert_notebooks_to_python_recursive(folder_path: str) -> None:
    """
    Recursively converts all Jupyter notebooks in a specified folder and its subfolders to Python files,
    saves the Python files in the same folder, and deletes the original notebook files.

    Args:
    - folder_path (str): The path to the folder containing the Jupyter notebooks to convert.

    Returns:
    - None
    """
    # exporter = PythonExporter()
    pattern = '.ipynb'
    notebook_paths = find_notebooks_recursive(folder_path, pattern)
    print(f"Number of notebooks: {len(notebook_paths)}")
    for notebook_path in notebook_paths:
        python_path = os.path.splitext(notebook_path)[0] + '.py'
        try:
            with open(notebook_path, 'r', encoding='utf-8') as nb_file:
                notebook = nbformat.read(nb_file, as_version=nbformat.NO_CONVERT)
                print(f"Converting {notebook_path}")
                python_code = ''
                for cell in notebook['cells']:
                    if cell['cell_type'] == 'code':
                        python_code += cell['source'] + '\n'
                if python_code:
                    with open(python_path, 'w', encoding='utf-8') as py_file:
                        py_file.write(python_code)
                    print(f"Saving {python_code}")
        except Exception as e:
            print(f"Error on {notebook_path} : {e}")

        os.remove(notebook_path)