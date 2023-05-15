import csv
import os
import random
from typing import List, Any, Dict
import requests
from config.constant import GitHub_CONFIG, PATH_FILE
from util.log import configure_logger
from util.requests_timer import delay_next_request

logger = configure_logger('github-data_logger', 'logging_file.log')
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root


def get_developer_logins(repos: List[str]) -> List[str]:
    developer_logins = []
    headers = {"Authorization": f"Bearer {random.choice(GitHub_CONFIG['token'])}"}
    for repo in repos:
        try:
            delay_next_request()
            response = requests.get(f"https://api.github.com/repos/{repo}/contributors", headers=headers)
            if response.status_code == 200:
                # print(response.status_code)
                contributors = response.json()
                for contributor in contributors:
                    # print(contributor)
                    developer_login = contributor['login']
                    print(developer_login)
                    developer_logins.append(developer_login)
            else:
                continue
        except ConnectionError as con:
            logger.error(f"An error occurred while collecting contributors login: {con}")
            continue
    return developer_logins


def get_developer_emails(usernames: List[str]) -> List[Dict[str, str]]:
    headers = {"Authorization": f"Bearer {random.choice(GitHub_CONFIG['token'])}"}
    emails = []
    for username in usernames:
        delay_next_request()
        url = f'https://api.github.com/users/{username}/events/public'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue

        events = response.json()
        found_push_event = False
        for event in events:
            if event['type'] == 'PushEvent' and 'commits' in event['payload']:
                found_push_event = True
                for commit in event['payload']['commits']:
                    email = commit['author'].get('email')
                    if email and email not in emails:
                        print(username, email)
                        emails.append({'username': username, 'email': email})
        if not found_push_event:
            continue

    return emails


def save_emails_to_csv(emails: List[Dict[str, str]]):
    fieldnames = ['username', 'email']

    unique_emails = []
    for email in emails:
        if email not in unique_emails:
            unique_emails.append(email)

    with open(ROOT_DIR + '/' + PATH_FILE['data'] + 'developper_info.csv', 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_emails)
    logger.info("Data saved to developper_info.csv")