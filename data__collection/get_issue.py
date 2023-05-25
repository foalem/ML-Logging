import csv
import os
import random
from util.log import configure_logger
from config.constant import GitHub_CONFIG, PATH_FILE
import requests
from typing import List, Dict
from util.requests_timer import delay_next_request

logger = configure_logger('github-data_logger', 'logging_file.log')
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root


def get_repository_issues(repos: List[str]) -> List[Dict[str, str]]:
    headers = {"Authorization": f"Bearer {random.choice(GitHub_CONFIG['token'])}"}
    issues = []

    for repo in repos:
        page = 1
        while True:
            delay_next_request()
            url = f'https://api.github.com/repos/{repo}/issues?state=all&page={page}&per_page=100'
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                page_issues = response.json()
                if len(page_issues) == 0:
                    break
                for issue in page_issues:
                    if issue['title'] == 'Fix example file path':
                        continue
                    logger.info(f"Collecting issue: {issue['title']}")
                    issue_data = {'title': issue['title'], 'body': issue['body']}
                    issues.append(issue_data)
                page += 1
            else:
                continue

    return issues


def save_issues_to_csv(issues):
    fieldnames = ['title', 'body']

    with open(ROOT_DIR + '/' + PATH_FILE['data'] + 'issue.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(issues)

    logger.info("Data saved to developper_info.csv")
