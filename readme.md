# Code Documentation

This code retrieves and processes data from the LOLDrivers API. It allows you to specify the API URL, the file name to save the retrieved data, the headers file to store the API headers, and additional file paths containing lists of functions.

## Prerequisites

- Python 3.x
- Required packages: argparse, json, logging, os, datetime, requests

## Usage

```bash
python finder.py [--api-url API_URL] [--file-name FILE_NAME] [--headers-file HEADERS_FILE] [file_paths [file_paths ...]]
```

- `--api-url`: URL of the API to retrieve data from (default: "https://www.loldrivers.io/api/drivers.json").
- `--file-name`: Name of the file to save the retrieved data (default: "drivers.json").
- `--headers-file`: Name of the file to save the API headers (default: "headers.json").
- `file_paths`: Paths to files containing lists of functions. If no file paths are provided, default lists of terminate functions and open functions will be used.

## Main functions

### `check_data_changed(api_url, file_name, headers_file)`
Check if the API data has changed since the last retrieval. If the data file is not present or the content has changed, download the file.

- `api_url`: URL of the API to retrieve data from.
- `file_name`: Name of the file to save the retrieved data.
- `headers_file`: Name of the file to save the API headers.

### `process_data(drivers_data, functions_list=None)`
Process the drivers' data based on the provided functions list.

- `drivers_data`: List of drivers' data obtained from the API.
- `functions_list`: List of function lists used for processing. If not provided or empty, default lists will be used.
- `desired_keys`: List of keys used for search. If not provided or empty, default 'filename' and 'md5' will be used.

### `main(api_url, file_name, headers_file, file_paths)`
Main function to retrieve and process data from the LOLDrivers API.

- `api_url`: URL of the API to retrieve data from.
- `file_name`: Name of the file to save the retrieved data.
- `headers_file`: Name of the file to save the API headers.
- `file_paths`: Paths to files containing lists of functions.

## Example usage:

```bash
python finder.py --file-name drivers.json --headers-file headers.json terminate_functions.txt open_functions.txt
```

Retrieves data from the LOLDrivers API, saves it to the "drivers.json" file, and saves the API headers to the "headers.json" file. It also processes the data using function lists provided in the "terminate_functions.txt" and "open_functions.txt" files.
