import argparse
import json
import logging
import os
from datetime import datetime
from requests import head, get, ConnectionError, Timeout

API_URL = "https://www.loldrivers.io/api/drivers.json"
FILE_NAME = "drivers.json"
HEADERS_FILE = "headers.json"
TERMINATE_FUNCTIONS = ["ZwTerminateProcess", "NtTerminateProcess"]
OPEN_FUNCTIONS = ["ZwOpenProcess", "NtOpenProcess"]
TIMEOUT = 5


def load_json(file_path):
	"""
	Load JSON data from a file.
	"""
	try:
		with open(file_path, "r", encoding="utf-8") as file:
			return json.load(file)
	except FileNotFoundError:
		return -1
	except json.JSONDecodeError as e:
		logging.error(f"Failed to decode JSON data from '{file_path}': {e}")
		return -2


def save_json(data, file_path):
	"""
	Save data as JSON to a file.
	"""
	try:
		with open(file_path, "w", encoding="utf-8") as file:
			json.dump(data, file, indent=4)
		logging.info(f"Data saved to '{file_path}'.")
		return True
	except Exception as e:
		logging.error(f"Failed to save data to '{file_path}': {e}")
		return False


def check_data_changed(api_url):
	"""
	Check if the API data has changed since the last retrieval.
	If the data file is not present or the content has changed, download the file.
	"""
	saved_headers = load_json(HEADERS_FILE)
	if saved_headers == -1:
		logging.info(f"Headers file not found. Redownloading.")

	

	try:
		response = head(api_url, timeout=TIMEOUT)
	except (ConnectionError, Timeout) as exception:
		logging.error(f"Connection error. No internet connection?")
		logging.info(f"Using local version of drivers.json")
		return False
	
	current_headers = {
		"ETag": response.headers.get("ETag"),
		"Last-Modified": response.headers.get("Last-Modified"),
	}

	if current_headers == saved_headers:
		logging.info("Data has not changed.")
		return False

	try:
		response = get(api_url)
		response.raise_for_status()
		data = response.json()
		save_json(data, FILE_NAME)
		save_json(current_headers, HEADERS_FILE)
		return True
	except Exception as e:
		logging.error(f"Failed to download data from '{api_url}': {e}")
		return False



def process_data(drivers_data, desired_keys=['filename', 'md5']):

	functions_list = [TERMINATE_FUNCTIONS, OPEN_FUNCTIONS]
	processed_data = {}
	for driver in drivers_data:
		for sample in driver.get("KnownVulnerableSamples", []):
			imported_functions = set(sample.get("ImportedFunctions", []))
			if all(
				any(func in imported_functions for func in func_list)
				for func_list in functions_list
			):
				driver_id = driver.get("Id")
				if driver_id not in processed_data:
					processed_data[driver_id] = {dk : [] for dk in desired_keys}
				for key in sample:
					lowered_key = key.lower()
					if lowered_key in desired_keys:
						processed_data[driver_id][lowered_key].append(sample.get(key))
	
	print(json.dumps(processed_data, indent=4))
	return processed_data


def main(api_url):
	"""
	Main function to retrieve and process data from LOLDrivers API.
	"""
	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

	check_data_changed(api_url)


	try:
		drivers_data = load_json(FILE_NAME)
		processed_data = process_data(drivers_data)
		if processed_data:
			output_file = os.path.splitext(FILE_NAME)[0] + "_processed.json"
			if save_json(processed_data, output_file):
				logging.info(f"Processed data saved to '{output_file}'.")
			else:
				logging.error("Failed to save processed data.")
	except json.JSONDecodeError as e:
		logging.error(f"Failed to decode JSON data from '{FILE_NAME}': {e}")


if __name__ == "__main__":
	# Configure argparse
	parser = argparse.ArgumentParser(
		description="Retrieve and process data from LOLDrivers API"
	)
	parser.add_argument(
		"--api-url",
		type=str,
		default=API_URL,
		help="URL of the API to retrieve data from",
	)

	args = parser.parse_args()

	# Run the main function
	main(args.api_url)
