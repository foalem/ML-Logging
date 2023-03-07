from util.util import *


def save_repo_find(file: str) -> None:
    """
    This function reads a directory, gets all the json files, reads the data from those files,
    and saves the data to a CSV file.
    file (str) : The path of the directory that needs to be read
    """
    data_list = []
    list_file = get_json_files(file)
    for filename in list_file:
        json_list = read_json(filename)
        data_list.extend(json_list)
    save_to_csv(data_list, list_file)
