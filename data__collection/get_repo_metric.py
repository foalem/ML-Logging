import csv
import os
import random
from typing import List, Any
from urllib.parse import urlparse, parse_qs

import requests

from config.constant import GitHub_CONFIG, PATH_FILE
from util.log import configure_logger
from util.requests_timer import delay_next_request

logger = configure_logger('github-data_logger', 'logging_file.log')
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root


def get_distinct_repo_names(file: str) -> List[str]:
    """
    This function reads a CSV file, gets the repository_full_name column, removes duplicate
    repository_full_name information and returns a list of distinct repository_full_name.
    file (str) : The path of the CSV file that needs to be read
    """
    repo_names = set()
    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            repo_names.add(row['repository_full_name'])
    return list(repo_names)


def get_contributors_count(repo_list: List[str]) -> List[int]:
    """
    This function returns the total number of contributors for a list of repositories using GitHub API
    repo_list (List[str]) : The list of repository names in the format 'username/repo_name'
    """
    headers = {"Authorization": f"Bearer {random.choice(GitHub_CONFIG['token'])}"}
    contributors_count_list = []
    for repo_name in repo_list:
        url = f"https://api.github.com/repos/{repo_name}/contributors"
        delay_next_request()
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                contributors_count_list.append(len(data))
                logger.info(f"number of contributor {len(data)}")
            else:
                continue
        except ConnectionError as con:
            logger.error(f"An error occurred while collecting repo contributors: {con}")
    return contributors_count_list


def get_repo_info(repo_list: List[str]) -> tuple[list[Any], list[Any], list[Any], list[Any], list[Any]]:
    """
    This function returns the total number of stars, created date, description, and language for a list of
    repositories using GitHub API repo_list (List[str]) : The list of repository names in the format
    'username/repo_name'
    """
    headers = {"Authorization": f"Bearer {random.choice(GitHub_CONFIG['token'])}"}
    stars_count_list = []
    created_date_list = []
    description_list = []
    language_list = []
    size_list = []
    for repo_name in repo_list:
        url = f"https://api.github.com/repos/{repo_name}"
        delay_next_request()
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                stars_count_list.append(data["stargazers_count"])
                size_list.append(data["size"])
                created_date_list.append(data["created_at"])
                description_list.append(data["description"])
                language_list.append(data["language"])
                logger.info(data["stargazers_count"])
            else:
                continue
        except ConnectionError as con:
            logger.error(f"An error occurred while collecting repo info: {con}")
    return stars_count_list, created_date_list, description_list, language_list, size_list


def get_commits_count(repo_list: List[str]) -> List[int]:
    """
    This function returns the total number of commits for a list of repositories using GitHub API
    repo_list (List[str]) : The list of repository names in the format 'username/repo_name'
    https://stackoverflow.com/a/45727280/10739430
    https://brianli.com/2022/07/python-get-number-of-commits-github-repository/
    """
    headers = {"Authorization": f"Bearer {random.choice(GitHub_CONFIG['token'])}"}
    commits_count_list = []
    const = 0
    for repo_name in repo_list:
        logger.info(repo_name)
        url = f"https://api.github.com/repos/{repo_name}/commits?sha=master&per_page=1&page=1"
        try:
            delay_next_request()
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                links = response.headers['Link']
                if links:
                    last_link = [link for link in links.split(",") if "rel=\"last\"" in link]
                    if last_link:
                        last_link_url = last_link[0].split(";")[0].strip()
                        last_link_url_args = parse_qs(urlparse(last_link_url).query)
                        commits_count = int(last_link_url_args["page"][0].strip(">"))
                        logger.info(commits_count)
                        commits_count_list.append(int(commits_count))
            else:
                logger.info(len(commits_count_list))
                commits_count_list.append(const)
        except ConnectionError as con:
            logger.error(f"An error occurred while collecting repo commit: {con}")
    return commits_count_list


def save_metric(rep_list_: List[str], contrib_list: List[int], star_list: List[int], created_list: List[str],
                descript_list: List[str], lang_list: List[str], com_list: List[int], sloc_list: List[int]) -> None:
    headers = ['repo_name', 'number_contributor', 'number_stars', 'created_date',
               'description', 'language', 'number_commit', 'sloc']
    rows = []
    for i in range(len(star_list)):
        row = [rep_list_[i], contrib_list[i], star_list[i],
               created_list[i], descript_list[i], lang_list[i], com_list[i], sloc_list[i]]
        rows.append(row)
    with open(ROOT_DIR + '/' + PATH_FILE['data'] + 'repo_meta_data.csv', 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        csv_writer.writerows(rows)
    logger.info("Data saved to output.csv")


