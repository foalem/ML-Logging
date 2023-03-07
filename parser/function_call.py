import ast
import csv
import os
import sys

from config.constant import PATH_FILE, LIBRARY_CONFIG
from util.log import configure_logger
from util.util import find_notebooks_recursive

logger = configure_logger('github-data_logger', 'logging_file.log')
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.imported_libraries = {}
        self.file_path = file_path
        self.calls = []

    def get_library_name(self, node):
        if isinstance(node, ast.Name):
            if node.id in self.imported_libraries:
                return self.imported_libraries[node.id]
        elif isinstance(node, ast.Attribute):
            library_name = self.get_library_name(node.value)
            if library_name is not None:
                return f"{library_name}.{node.attr}"
        return None

    def get_function_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            function_name = self.get_function_name(node.value)
            if function_name is not None:
                return f"{function_name}.{node.attr}"
        return None

    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname is not None:
                self.imported_libraries[alias.asname] = alias.name
            else:
                self.imported_libraries[alias.name.split('.')[0]] = alias.name

    def visit_ImportFrom(self, node):
        module_name = node.module or ''
        for alias in node.names:
            if alias.asname is not None:
                self.imported_libraries[alias.asname] = f"{module_name}.{alias.name}"
            else:
                parts = alias.name.split('.')
                self.imported_libraries[parts[0]] = f"{module_name}.{alias.name}"
                for i in range(1, len(parts)):
                    key = ".".join(parts[:i + 1])
                    value = f"{module_name}.{alias.name}" + "." + ".".join(parts[i + 1:])
                    self.imported_libraries[key] = value

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            library_name = self.get_library_name(node.func)
            function_name = self.get_function_name(node.func)
            if library_name is not None and function_name is not None:
                self.calls.append({
                    "library": library_name,
                    "function": function_name,
                    "line": node.lineno,
                    "file": self.file_path
                })
        elif isinstance(node.func, ast.Name):
            # Check if the function call is inside a class or a function
            if not any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) for n in ast.walk(node)):
                function_name = node.func.id
                if function_name in self.imported_libraries:
                    library_name = self.imported_libraries[function_name]
                    self.calls.append({
                        "library": library_name,
                        "function": function_name,
                        "line": node.lineno,
                        "file": self.file_path
                    })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # visit the function call inside the class
        for item in node.body:
            self.visit(item)

    def visit_FunctionDef(self, node):
        # visit the function call inside the function
        for item in node.body:
            self.visit(item)

    def get_calls(self, tree):
        self.visit(tree)
        return self.calls


def filter_libs(first_list, second_list, csv_filename):
    libs = set(first_list)
    # filtered_list = [elem for elem in second_list if elem['library'] in libs]
    filtered_list = [elem for elem in second_list if any(lib in elem['library'] for lib in libs)]
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['library', 'function', 'line', 'file'])
            for elem in filtered_list:
                writer.writerow(
                    [elem['library'], elem['function'], elem['line'], elem['file']])
    except Exception as e:
        print(f"Failed to open file error: {e}")


# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     file_path = "C:/Users/fpatr/PycharmProjects/Fairness-library-paper/data/clones/abnormal-distribution" \
#                 "/AC295_abnormal-distribution/submissions/practicum2_Abnormal-Distribution/BasicModel_Final.py "
#     pattern = '.py'
#     python_paths = find_notebooks_recursive(f"{ROOT_DIR}{PATH_FILE['data']}clones", pattern)
#     all_call_function = []
#     for filepath in python_paths:
#         with open(filepath, encoding='utf-8') as f:
#             code = f.read()
#         tree = ast.parse(code)
#         visitor = FunctionCallVisitor(file_path)
#         calls = visitor.get_calls(tree)
#         all_call_function.extend(calls)
#     libraries_to_track = LIBRARY_CONFIG["import"]
#     filter_libs(libraries_to_track, all_call_function, ROOT_DIR + '/' + PATH_FILE['data'] + 'call_function.csv')
#
#     print(calls)

