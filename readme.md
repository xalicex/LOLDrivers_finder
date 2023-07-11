# Process killer drivers finder

The purpose of this project is to retrieve potential process killer drivers. 

It uses the `imported functions` attribute of the `drivers.json` file available on the [LOLDrivers project](https://www.loldrivers.io).

To do so, the code will select all drivers importing the `Nt/ZwOpenProcess` AND `Nt/ZwTerminateProcess`.

Which means only drivers importing one of the `*OpenProcess` AND one of the `*TerminatedProcess` functions will be retrieved.

All the drivers retrieved by the script are POTENTIAL process killer drivers. It means that some of them aren't.

Of course, function can be imported dynamically, processes can be terminated other ways and handle retrieved without using `Nt/ZwOpenProcess`. 

This script is not bullet proof. It's just a quick and dirty way to find easy targets, so it's 100% sure that it will miss some real process drivers killer drivers available on LOLDrivers.

However, in the list of drivers retrieved by the script today, some of them are indeed process killer drivers. So have fun !




## Prerequisites

- Python 3.x
- Required packages: argparse, json, logging, os, datetime, requests

## Usage

```bash
python finder.py [--api-url API_URL]
```

- `--api-url`: URL of the API to lretrieve data from (default: "https://www.loldrivers.io/api/drivers.json").

## Main functions

### `check_data_changed(api_url)`
Check if the API data has changed since the last retrieval. If the data file is not present or the content has changed, download the file.

- `api_url`: URL of the API to retrieve data from.

### `process_data(drivers_data)`
Process the drivers' data based on the provided functions list.

- `drivers_data`: List of drivers' data obtained from the API.
- `desired_keys`: List of keys used for search. If not provided or empty, default 'filename' and 'md5' will be used.

### `main(api_url)`
Main function to retrieve and process data from the LOLDrivers API.

- `api_url`: URL of the API to retrieve data from.

## Example usage:

Basic usage:

```bash
python finder.py
```

Setting a specific URL where to download the driver.json file:

```bash
python finder.py  --api-url https://www.loldrivers.io/api/drivers.json
```

Retrieves data from the LOLDrivers API, saves it to the "drivers.json" file, and saves the API headers to the "headers.json" file. 

---
Thanks to [@OMGhozlan](https://github.com/OMGhozlan) for his contribution on the code refactoring ! 
