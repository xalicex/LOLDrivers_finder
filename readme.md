# Process killer drivers finder

The purpose of this project is to retrieve potential process killer drivers. 

It uses the `imported functions` attribute of the `drivers.json` file available on the [LOLDrivers project](https://www.loldrivers.io).

To do so, the code will select all drivers importing the `Nt/ZwOpenProcess` AND `Nt/ZwTerminateProcess`.

Which means only drivers importing one of the `*OpenProcess` AND one of the `*TerminatedProcess` functions will be retrieved.

All the drivers retrieved by the script are POTENTIAL process killer drivers. It means that some of them aren't.

Of course, function can be imported dynamically, processes can be terminated other ways and handle retrieved without using `Nt/ZwOpenProcess`. This script is not bullet proof. It's just a quick and dirty way to find easy targets.

When executed, this code will check if a new version of `drivers.json` is available on LOLDrivers and download it.



## Prerequisites

- Python 3.x
- Required packages: argparse, json, logging, os, datetime, requests

## Usage

```bash
python finder.py [--api-url API_URL] [file_paths [file_paths ...]]
```

- `--api-url`: URL of the API to lretrieve data from (default: "https://www.loldrivers.io/api/drivers.json").
- `file_paths`: Paths to files containing lists of functions. If no file paths are provided, default lists of terminate functions and open functions will be used.

## Main functions

### `check_data_changed(api_url)`
Check if the API data has changed since the last retrieval. If the data file is not present or the content has changed, download the file.

- `api_url`: URL of the API to retrieve data from.

### `process_data(drivers_data, functions_list=None)`
Process the drivers' data based on the provided functions list.

- `drivers_data`: List of drivers' data obtained from the API.
- `functions_list`: List of function lists used for processing. If not provided or empty, default lists will be used.
- `desired_keys`: List of keys used for search. If not provided or empty, default 'filename' and 'md5' will be used.

### `main(api_url, file_paths)`
Main function to retrieve and process data from the LOLDrivers API.

- `api_url`: URL of the API to retrieve data from.
- `file_paths`: Paths to files containing lists of functions.

## Example usage:

Basic usage:

```bash
python finder.py
```

Setting a specific URL where to download the driver.json file:


```bash
python finder.py  --api-url https://www.loldrivers.io/api/drivers.json
```

Setting specifics lists of functions (be sure to understand in the code how this function will be processed and searched !!!):
```bash
python finder.py functions_list_A.txt functions_list_B.txt
```

Retrieves data from the LOLDrivers API, saves it to the "drivers.json" file, and saves the API headers to the "headers.json" file. It also processes the data using function lists provided in the "functions_list_A.txt" and "functions_list_B.txt" files.

---
Thanks to [@OMGhozlan](https://github.com/OMGhozlan) for his contribution on the code refactoring ! 
