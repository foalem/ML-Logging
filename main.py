import argparse
import ast
import os.path
import sys

from data__collection.compute_project_size import save_lines_of_code_to_csv
from data__collection.get_repo import *
from data__collection.get_repo_infos import *
from data__collection.get_repo_metric import *
from config.constant import *
from data__collection.clone_repo import *
from parser.convert_notebooks_python import convert_notebooks_to_python_recursive
from parser.convert_python_2_to_3 import remove_lines
from parser.function_call import FunctionCallVisitor, filter_libs

logger = configure_logger("github-data_logger", 'logging_file.log')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root


def main() -> None:
    parser = argparse.ArgumentParser(
        description='description'
    )

    parser.add_argument('-c', '--collect', help="Search repository with some configuration", dest='DATA',
                        required=False,
                        action='store_true')
    parser.add_argument('-s', '--save', help="Save repository found", dest='SAVE', required=False,
                        action='store_true')
    parser.add_argument('-m', '--metric', help="Collect repository metric", dest='METRIC', required=False,
                        action='store_true')
    parser.add_argument('-cl', '--clone', help="Clone repository", dest='CLONE', required=False,
                        action='store_true')
    parser.add_argument('-conv', '--convert', help="Convert all notebook file in a repository in .py file",
                        dest='CONVERT', required=False, action='store_true')
    parser.add_argument('-p', '--parser', help="Parse Python file and extract all function call",
                        dest='PARSER', required=False, action='store_true'),
    parser.add_argument('-sloc', '--codesize', help="Compute size of Python code in a repository",
                        dest='CODESIZE', required=False, action='store_true')
    args = parser.parse_args()
    if args.DATA:
        collect_repo()
    if args.SAVE:
        save_repo_find(ROOT_DIR + '/' + PATH_FILE['data'])
    if args.METRIC:
        repo_list_ = get_distinct_repo_names(f"{ROOT_DIR}{PATH_FILE['data']}repo_0.csv")
        commits_count_list_ = get_commits_count(repo_list_)
        contributor_list = get_contributors_count(repo_list_)
        stars_list, created_date_list_, description_list_, language_list_, size_list_ = get_repo_info(repo_list_)
        save_metric(repo_list_, contributor_list, stars_list, created_date_list_,
                    description_list_, language_list_, commits_count_list_, size_list_)
    if args.CLONE:
        repo__list = read_repos_from_csv(f"{ROOT_DIR}{PATH_FILE['data']}repo_data_fitered4.csv")
        print(repo__list)
        clone_repos(repo__list, f"{ROOT_DIR}{PATH_FILE['data']}clones")

    if args.CONVERT:
        convert_notebooks_to_python_recursive(f"{ROOT_DIR}{PATH_FILE['data']}clones")

    if args.PARSER:
        remove_lines(f"{ROOT_DIR}{PATH_FILE['data']}clones")
        logger.info("Finish removing regex and refactor the code to python 3")
        # sys.exit()
        pattern = '.py'
        python_paths = find_notebooks_recursive(f"{ROOT_DIR}{PATH_FILE['data']}clones", pattern)
        all_call_function = []
        for file_path in python_paths:
            sys.setrecursionlimit(10000)
            try:
                with open(file_path, encoding='utf-8') as f:
                    code = f.read()
                    tree = ast.parse(code)
                    visitor = FunctionCallVisitor(file_path)
                    calls = visitor.get_calls(tree)
                    all_call_function.extend(calls)
            except Exception as e:
                print(f"Error on {file_path} : {e}")
        libraries_to_track = LIBRARY_CONFIG["import"]
        logger.info("saving logging function call")
        filter_libs(libraries_to_track, all_call_function, ROOT_DIR + '/' + PATH_FILE['data'] + 'loggging_call_function5.csv')
        # __function_call = find_library_function_calls(f"{ROOT_DIR}{PATH_FILE['data']}clones", lib_)
        # print(__function_call)
    if args.CODESIZE:
        project_path = os.path.join(f"{ROOT_DIR}{PATH_FILE['data']}clones")
        project_list = list_subfolders(project_path)
        save_lines_of_code_to_csv(project_list, f"{ROOT_DIR}{PATH_FILE['data']}project_size_final.csv")


if __name__ == '__main__':
    main()
