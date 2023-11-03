# Project: Replication Study of "Studying Logging Practice in Machine Learning-based Applications"

This repository contains a Python script for conducting a replication study of the paper titled "Studying Logging Practice in Machine Learning-based Applications." The script enables you to collect data from GitHub repositories, perform various analyses, and save the results. This README provides an overview of the project and instructions for using the script.

## Prerequisites

Before using this script, make sure you have the following prerequisites:

- Python 3.x installed.
- Required Python packages installed. You can install them using `pip install -r requirements.txt`, where `requirements.txt` contains the necessary packages.

## Usage

To run the script, use the following command:

```
python main.py [options]
```
## Options
```
-c or --collect: Search for repositories with specified configurations.
-s or --save: Save the found repositories to a file.
-m or --metric: Collect metric data for the repositories.
-cl or --clone: Clone the repositories.
-conv or --convert: Convert notebook files to Python files in the cloned repositories.
-p or --parser: Parse Python files and extract all function calls.
-sloc or --codesize: Compute the size of Python code in a repository.
-d or --dev: Collect developer email information.
-i or --issue: Collect issue information.
```
## Example Usage
To search for repositories with specified configurations and save them to a file:
```
python main.py -c -s
```
To collect metric data for the repositories:
```
python main.py -m
```
To clone the repositories:
```
python main.py -cl
```
To convert notebook files to Python files in the cloned repositories:
```
python main.py -conv
```
To parse Python files and extract function calls:
```
python main.py -p
```
To compute the size of Python code in a repository:
```
python main.py -sloc
```
To collect developer email information:
```
python main.py -d
```
To collect issue information:
```
python main.py -i
```
# Function Descriptions
Search for Repositories (-c or --collect):
- This function searches for GitHub repositories based on specified configurations.

Save Repositories (-s or --save):
- Saves the found repositories to a file.

Collect Repository Metric Data (-m or --metric):
- Collects metric data for the repositories, including commit counts, contributor counts, stars, created dates, descriptions, languages, and repository sizes.

Clone Repositories (-cl or --clone):
- Clones the repositories to a local directory.

Convert Notebook Files to Python Files (-conv or --convert):
- Recursively converts Jupyter notebook files to Python files in the cloned repositories.

Parse Python Files and Extract Function Calls (-p or --parser):
- Parses Python files, extracts function calls, and saves them in a CSV file.

Compute Python Code Size (-sloc or --codesize):
- Computes the size of Python code in the cloned repositories and saves the results in a CSV file.

Collect Developer Email Information (-d or --dev):
- Collects developer email information from the repositories and saves it in a CSV file.

Collect Issue Information (-i or --issue):
- Collects issue information from the repositories and saves it in a CSV file.

# Output Files
The script generates various output files based on the chosen options. Output files are saved in the specified directory or the project root.

# Conclusion
This Python script provides a comprehensive set of tools for conducting a replication study of the paper "Studying Logging Practice in Machine Learning-based Applications." By using the provided command-line options, you can customize the data collection and analysis process to suit your needs.