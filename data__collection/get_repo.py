import requests
from config.constant import *
from util.requests_timer import *
from util.util import *
from util.log import *

logger = configure_logger('github-data_logger', 'logging_file.log')


def search_repositories(query) -> List:
    """
    Search for repositories that matches query
    :param query: string, search query
    """
    # Set the API endpoint URL
    url = f'https://api.github.com/search/code?q=' + query + '+in:file+size:>=0+language:python'

    # Initialize the page number
    page = 1

    # Initialize an empty list to store the search results
    results = []

    while True:
        # Set the pagination parameters
        params = {
            "page": page,
            "per_page": GitHub_CONFIG['per_page']
        }

        # Set the HTTP headers
        headers = {
            "Authorization": f"Bearer {random.choice(GitHub_CONFIG['token'])}",
            "Accept": "application/vnd.github+json"
        }

        try:
            # Send the HTTP request
            response = requests.get(url, headers=headers, params=params)
            if response.text:
                # If the request was successful, update the URL and append the results
                logger.info(f"page number: {page}")
                if page <= GitHub_CONFIG['max_page']:
                    if response.status_code == 200:
                        logger.info("Successfully get repo")
                        data = response.json()
                        logger.info(f"total result: {data['total_count']}")
                        if len(results) == data['total_count'] or len(data["items"]) == 0:
                            break
                        results.extend(data["items"])
                    else:
                        pass
                        logger.info(
                            f"Failed to retrieve repository information. HTTP status code: {response.status_code}")
                else:
                    logger.info(f"Number of page attend {page}")
                    break
            else:
                logger.warning("response is empty")
                break
            # delay
            delay_next_request()
            # Increment the page number
            page += 1
        except ConnectionError:
            logger.error("An error occurred while collecting repo")
    return results


def collect_repo() -> None:
    for conf in REPO_CONFIG['import']:
        query = f"{conf}"
        print(query)
        json_list = search_repositories(query)
        save_to_json(json_list, PATH_FILE['data'] + '{}.json'.format(conf))
        delay_next_request()
