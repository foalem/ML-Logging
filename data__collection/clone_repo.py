import csv
import os
import subprocess
from typing import List, Dict

from util.log import configure_logger

logger = configure_logger('github-data_logger', 'logging_file.log')


def read_repos_from_csv(csv_path: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file containing repository information and returns a list of dictionaries.

    Args:
    - csv_path (str): The path to the CSV file.

    Returns:
    - A list of dictionaries containing the repository information, where each dictionary represents a row in the CSV.
    """
    repos = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            repos.append(row)
    return repos


def clone_repos(repos: List[Dict[str, str]], target_folder: str) -> None:
    """
    Clones a list of GitHub repositories to a specified target folder.

    Args: - repos (list of dict): A list of dictionaries containing the repository information, as returned by
    read_repos_from_csv(). - target_folder (str): The path to the target folder where the repositories should be
    cloned.

    Returns:
    - None
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for repo in repos:
        repo_folder = os.path.join(target_folder, repo['Repos'])
        if not os.path.exists(repo_folder):
            os.makedirs(repo_folder)
        result = subprocess.call(['git', 'clone', f'https://github.com/{repo["Repos"]}.git', repo_folder])
        if result == 0:
            logger.info(f'Successfully cloned {repo["Repos"]} into {repo_folder}.')
        else:
            logger.info(f'Error cloning {repo["Repos"]}.')
