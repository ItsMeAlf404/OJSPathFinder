import requests, concurrent.futures
from urllib.parse import urljoin
from colorama import Fore, init
import os
import pyfiglet  # pip install pyfiglet

init(autoreset=True)

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    ascii_banner = pyfiglet.figlet_format("OJS Path Checker")
    print(Fore.GREEN + ascii_banner)
    print(Fore.LIGHTBLACK_EX + "      Automatic Scan Directory Path Open Journals System\n      Author: @yourdre4m7")
    print(Fore.LIGHTBLACK_EX + "=" * 60)

def load_file(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scan_path(target, paths, check_index=False):
    for path in paths:
        full_url = "https://" + target + path
        try:
            r = requests.get(full_url, timeout=10)
            if r.status_code == 200:
                if check_index and "Index of" in r.text:
                    print(Fore.GREEN + f"OPEN DIRECTORY >>> {full_url}")
                    with open("open_dir.txt", "a") as f:
                        f.write(full_url + "\n")
                else:
                    print(Fore.RED + f"NOT VALID PATH >>> {full_url}")
            elif r.status_code == 403:
                print(Fore.YELLOW + f"FORBIDDEN - MAYBE VULN >>> {full_url}")
                with open("forbidden.txt", "a") as f:
                    f.write(full_url + "\n")
        except Exception:
            pass

def run_scan():
    banner()
    list_file = input(Fore.LIGHTBLACK_EX + "Input Domain List >>> ").strip()
    path_file = input(Fore.LIGHTBLACK_EX + "Input Path Directory >>> ").strip()

    try:
        targets = load_file(list_file)
        paths = load_file(path_file)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Gagal membuka file: {e}")
        return

    print(Fore.CYAN + f"\n Mulai Scan {len(targets)} domain dengan {len(paths)} path...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for target in targets:
            executor.submit(scan_path, target, paths, True)

if __name__ == "__main__":
    run_scan()
