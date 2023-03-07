import csv
import subprocess
import json


def get_lines_of_code(project_path):
    cloc_command = ["cloc", "--json", project_path]
    result = subprocess.run(cloc_command, capture_output=True, text=True)

    # check if the subprocess ran correctly
    if result.returncode != 0:
        raise ValueError("Cloc command failed. Error message: " + result.stderr)

    cloc_data = json.loads(result.stdout)
    return cloc_data["SUM"]["code"]


def save_lines_of_code_to_csv(projects, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['project', 'lines_of_code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for project in projects:
            try:
                lines_of_code = get_lines_of_code(project)
                writer.writerow({'project': project, 'lines_of_code': lines_of_code})
            except Exception as e:
                print(f"Error processing {project}: {str(e)}")
