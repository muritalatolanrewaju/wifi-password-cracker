# Wi-Fi Brute Force Tool

This Python script provides a Wi-Fi brute-force attack tool for cracking WPA/WPA2 passwords. It uses a combination of PyWiFi, itertools, and tqdm libraries to manage Wi-Fi connections, generate password combinations, and display progress, respectively.

## Features

- **Automated Wi-Fi Password Generation**: Generates all possible numeric password combinations for a specified length.
- **Wi-Fi Interface Selection**: Allows users to select the Wi-Fi adapter to use for the attack.
- **Network Scanning**: Scans for available Wi-Fi networks and prompts the user to select a target network.
- **Brute-Force Attack**: Iterates through password combinations in random order to attempt connection to the target network.
- **Real-time Progress Monitoring**: Displays progress, time elapsed, and estimated time remaining during the attack.
- **Password File Support**: Option to create a password file or use an existing one.

## Requirements

- Python 3.x
- PyWiFi
- tqdm

## Usage

1. Clone the repository

```bash
git clone https://github.com/muritalatolanrewaju/Wi-Fi-Brute-Force-Tool.git
cd Wi-Fi-Brute-Force-Tool
```

2. Install required dependencies

```bash
pip install -r requirements.txt
```

3. Run the script and follow the on-screen instructions to perform the Wi-Fi brute-force attack.

## Command-line Arguments

- `-s` or `--ssid`: SSID (Wi-Fi Name) of the target network.
- `-d` or `--digits`: Number of digits for the password list (default is 8).
- `-f` or `--file`: Path to an existing password file. If not provided, a new password file will be generated.

## Password File

- If a password file is not provided via the command line, the script will prompt the user to generate a new one.
- The default password file name is `passwords_<digit_length>_digits.txt` and will be saved in the same directory as the script.

## Example Usage

```bash
python wifi_brute_force.py -s <SSID> -d <digits> -f <password_file>
```

```bash
python wifi_brute_force.py -s MyWiFi -d 8
```

```bash
python wifi_brute_force.py -s MyWiFi -d 8 -f rockyou.txt
```

## Disclaimer

This tool is intended for educational and research purposes only. The author is not responsible for any misuse of the information provided.