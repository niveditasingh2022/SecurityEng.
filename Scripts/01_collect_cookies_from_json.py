import os
import json
import csv
import logging
import argparse
import time
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

parser = argparse.ArgumentParser(description='Collect data from json files in a directory.')
parser.add_argument('directory', type=str, help='The directory to process json files.')
args = parser.parse_args()

if not args.directory:
    args.directory = input("Please enter the directory which includes json files: ")

logging.basicConfig(filename="21_collect_cookies_from_json.log", level=logging.INFO)

headers = ["Page", "Lifetime"]

result_data = []

for root, dirs, files in os.walk(args.directory):
    for file in files:
        if file.endswith(".json"):
            try:
                with open(os.path.join(root, file)) as json_file:
                    data = json.load(json_file)

                try:
                    cookies_data = data['first']['cookies']['cookies']
                    log_data = data['log']
                except KeyError as e:
                    logging.info(f"No 'first -> cookies -> cookies' or 'log' found in {file}. Error: {str(e)}")
                    continue

                if not cookies_data:
                    logging.info(f"Empty cookies data in {file}. Skipping this file.")
                    continue

                first_visit_time_str = next((log[0] for log in data['log'] if "Making First Visit to" in log[1]), None)
                if first_visit_time_str:
                    first_visit_time = time.mktime(time.strptime(first_visit_time_str, "%Y-%m-%d %H:%M:%S"))
                else:
                    first_visit_time = None

                visited_website = next((log[1].split("://")[-1].strip() for log in data['log'] if "Making First Visit to" in log[1]), None)

                file_name_without_extension = file.replace(".json", "")
                clean_filename = file_name_without_extension.replace('_', '/')
                if visited_website and clean_filename not in visited_website:
                    logging.info(f"File name {clean_filename} doesn't match with the visited website {visited_website}. Please check this file by yourself.")
                    #logging.info(f"File name {clean_filename} doesn't match with the visited website {visited_website}. Skipping this file.")
                    #continue
                
                for cookie in cookies_data:
                    page_data = defaultdict(str)
                    page_data["Page"] = clean_filename

                    for key, value in cookie.items():
                        if key not in headers:
                            headers.append(key)
                        page_data[key] = value

                    if 'expires' in cookie and first_visit_time:
                        if cookie['expires'] == -1:
                            page_data['Lifetime'] = 0
                        else:
                            page_data['Lifetime'] = int(cookie['expires'] - first_visit_time)
                    elif 'expires' not in cookie:
                        logging.warning(f"No 'expires' key in cookie data of {file}. Setting Lifetime as None.")
                        page_data['Lifetime'] = None

                    result_data.append(page_data)
            except Exception as e:
                logging.error(f"Error processing file {file}. Error: {str(e)}")

output_filename = args.directory.replace('/', '_').strip('_').strip() + '.csv'
with open(output_filename, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    for data in result_data:
        writer.writerow(data)
