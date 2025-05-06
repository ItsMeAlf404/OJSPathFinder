import requests
from colorama import Fore, Style, init
import pyfiglet
import argparse
import os

# Inisialisasi colorama
init(autoreset=True)

# Tampilkan banner
def tampilkan_banner():
    banner = pyfiglet.figlet_format("OJS Checker", font="slant")
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "Created by: t.me/yourdre4m7\n" + Style.RESET_ALL)

# Fungsi untuk memuat daftar dari file
def load_list(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[!] File '{file_name}' tidak ditemukan.")
        return []

# Fungsi pengecekan path
def cek_path(domain, paths):
    valid_paths = []
    print(Fore.CYAN + f"\n[✓] Mengecek domain: {domain}")
    
    for path in paths:
        url = domain.rstrip("/") + "/" + path.lstrip("/")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(Fore.GREEN + f"    [+] VALID     : {url}")
                valid_paths.append(url)
            elif response.status_code == 403:
                print(Fore.YELLOW + f"    [!] DIBLOK    : {url} (403 Forbidden)")
            elif response.status_code == 404:
                print(Fore.RED + f"    [x] TIDAK ADA : {url}")
            else:
                print(Fore.LIGHTBLUE_EX + f"    [?] STATUS {response.status_code}: {url}")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"    [!] ERROR saat mengakses {url}: {e}")
    
    return valid_paths

# Fungsi menyimpan hasil valid
def simpan_hasil(domain, valid_urls, file_out="hasil_path_valid.txt"):
    with open(file_out, "a", encoding="utf-8") as f:
        f.write(f"\n# Domain: {domain}\n")
        for url in valid_urls:
            f.write(url + "\n")

if __name__ == "__main__":
    tampilkan_banner()

    # Parsing argumen
    parser = argparse.ArgumentParser(description="Cek path OJS di banyak domain.")
    parser.add_argument("-d", "--domains", default="domains.txt", help="File berisi daftar domain (default: domains.txt)")
    parser.add_argument("-p", "--paths", default="pathlist.txt", help="File berisi daftar path (default: pathlist.txt)")
    args = parser.parse_args()

    if not os.path.exists(args.domains):
        print(Fore.RED + f"[!] File domain '{args.domains}' tidak ditemukan.")
        exit()

    if not os.path.exists(args.paths):
        print(Fore.RED + f"[!] File path '{args.paths}' tidak ditemukan.")
        exit()

    domains = load_list(args.domains)
    paths = load_list(args.paths)

    if not domains:
        print(Fore.RED + "[!] Daftar domain kosong.")
        exit()

    if not paths:
        print(Fore.RED + "[!] Daftar path kosong.")
        exit()

    for domain in domains:
        valid = cek_path(domain, paths)
        if valid:
            simpan_hasil(domain, valid)
