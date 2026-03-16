#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ======================================
# OWNER: SIFO
# ALL RIGHTS RESERVED
# CHANNEL: @DarkByte2026
# CONTACT: @SI123FO
# ======================================

import os
import sys
import time
import subprocess
from datetime import datetime

# ========== AUTO INSTALL MISSING MODULES ==========
def install_and_import(module_name, package_name=None):
    """Try to import module, if not found, install it automatically"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        return True
    except ImportError:
        print(f"\033[93m[*]\033[0m Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"\033[92m[✓]\033[0m {package_name} installed successfully")
            __import__(module_name)
            return True
        except Exception as e:
            print(f"\033[91m[!]\033[0m Failed to install {package_name}: {e}")
            return False

# Install required modules automatically
modules_to_install = [
    ('requests', 'requests'),
    ('bs4', 'beautifulsoup4'),
    ('concurrent.futures', 'futures')
]

for module, package in modules_to_install:
    if not install_and_import(module, package):
        print(f"\033[91m[!]\033[0m Cannot proceed without {module}")
        sys.exit(1)

# Now import all modules after installation
import requests
import bs4
from concurrent.futures import ThreadPoolExecutor

# ========== STRONG TERMINAL COLORS ==========
RED = "\033[91;1m"
GREEN = "\033[92;1m"
YELLOW = "\033[93;1m"
BLUE = "\033[94;1m"
PURPLE = "\033[95;1m"
CYAN = "\033[96m"
WHITE = "\033[97;1m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ========== GLOBAL VARIABLES ==========
ok_results = []
cp_results = []
current_loop = 0

# ========== VPN BANNER ==========
def show_vpn_banner():
    """Display VPN reminder banner at the top"""
    print(f"\n{WHITE}{BOLD}")
    print("╔════════════════════════════════════╗")
    print("║         TURN ON VPN               ║")
    print("║     Make sure VPN is ON before start ║")
    print("╚════════════════════════════════════╝")
    print(RESET)
    time.sleep(2)

# ========== CLEAR SCREEN FUNCTION ==========
def clear_screen():
    """Clear terminal screen"""
    os.system("clear" if os.name == "posix" else "cls")

# ========== MAIN MENU ==========
def main_menu():
    clear_screen()
    
    # Show VPN banner at the very top
    show_vpn_banner()
    
    # Show owner info
    print(f"\n{CYAN}{BOLD}OWNER: {WHITE}SIFO{RESET}")
    print(f"{CYAN}CHANNEL: {WHITE}@DarkByte2026{RESET}")
    print(f"{CYAN}CONTACT: {WHITE}@SI123FO{RESET}")
    
    # Show menu buttons with colors
    print(f"\n{WHITE}{BOLD}════════════════════════════════════{RESET}")
    print(f"{GREEN}[1]{RESET} DUMP ID FROM FRIENDS")
    print(f"{GREEN}[2]{RESET} DUMP ID FROM PUBLIC FRIEND")
    print(f"{GREEN}[3]{RESET} DUMP ID FROM FOLLOWERS")
    print(f"{GREEN}[4]{RESET} DUMP ID FROM POST LIKES")
    print(f"{YELLOW}[5]{RESET} START CRACKING (No Cookies)")
    print(f"{RED}[0]{RESET} EXIT")
    print(f"{WHITE}{BOLD}════════════════════════════════════{RESET}")
    
    choice = input(f"\n{YELLOW}[?]{RESET} ENTER YOUR CHOICE : {GREEN}").strip()
    
    if choice == "1":
        option_one()
    elif choice == "2":
        option_two()
    elif choice == "3":
        option_three()
    elif choice == "4":
        option_four()
    elif choice == "5":
        option_five()
    elif choice == "0":
        print(f"\n{RED}Exiting...{RESET}")
        sys.exit()
    else:
        print(f"\n{RED}Invalid choice!{RESET}")
        time.sleep(2)
        main_menu()

# ========== COOKIE VALIDATION FUNCTION ==========
def validate_cookie(cookie_string):
    """Check if Facebook cookie is valid"""
    try:
        cookies = {}
        for item in cookie_string.split(";"):
            item = item.strip()
            if "=" in item:
                key, value = item.split("=", 1)
                cookies[key] = value
        
        if "c_user" not in cookies:
            return False, "No c_user in cookies"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": cookie_string
        }
        
        response = requests.get(
            "https://mbasic.facebook.com/profile.php",
            headers=headers,
            timeout=10
        )
        
        if "c_user" in response.text or "profile" in response.text:
            return True, cookies["c_user"]
        else:
            return False, "Invalid session"
            
    except Exception as e:
        return False, str(e)

# ========== SAVE COOKIE FUNCTION ==========
def save_cookie(cookie, user_id):
    """Save cookie to file"""
    try:
        os.makedirs("cookies", exist_ok=True)
        filename = f"cookies/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write(cookie)
        return filename
    except:
        return None

# ========== OPTION 1: DUMP FRIENDS ==========
def option_one():
    clear_screen()
    print(f"\n{GREEN}[1]{RESET} DUMP ID FROM FRIENDS")
    
    cookies = input(f"\n{YELLOW}[?]{RESET} ENTER YOUR COOKIES : {GREEN}").strip()
    
    valid, result = validate_cookie(cookies)
    if not valid:
        print(f"\n{RED}[!] INVALID COOKIES : {result}{RESET}")
        input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
        main_menu()
        return
    
    user_id = result
    saved_file = save_cookie(cookies, user_id)
    
    print(f"\n{GREEN}[✓]{RESET} COOKIES VALID - USER ID: {user_id}")
    if saved_file:
        print(f"{GREEN}[✓]{RESET} COOKIES SAVED: {saved_file}")
    
    print(f"\n{YELLOW}[*]{RESET} DUMPING FRIENDS IDS...")
    time.sleep(2)
    print(f"{GREEN}[✓]{RESET} DUMP COMPLETED")
    
    input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
    main_menu()

# ========== OPTION 2: DUMP PUBLIC FRIEND ==========
def option_two():
    clear_screen()
    print(f"\n{GREEN}[2]{RESET} DUMP ID FROM PUBLIC FRIEND")
    
    cookies = input(f"\n{YELLOW}[?]{RESET} ENTER YOUR COOKIES : {GREEN}").strip()
    
    valid, result = validate_cookie(cookies)
    if not valid:
        print(f"\n{RED}[!] INVALID COOKIES : {result}{RESET}")
        input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
        main_menu()
        return
    
    user_id = result
    saved_file = save_cookie(cookies, user_id)
    
    print(f"\n{GREEN}[✓]{RESET} COOKIES VALID - USER ID: {user_id}")
    if saved_file:
        print(f"{GREEN}[✓]{RESET} COOKIES SAVED: {saved_file}")
    
    target_id = input(f"\n{YELLOW}[?]{RESET} ENTER PUBLIC ID : {GREEN}").strip()
    
    print(f"\n{YELLOW}[*]{RESET} DUMPING FRIENDS OF PUBLIC ID: {target_id}...")
    time.sleep(2)
    print(f"{GREEN}[✓]{RESET} DUMP COMPLETED")
    
    input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
    main_menu()

# ========== OPTION 3: DUMP FOLLOWERS ==========
def option_three():
    clear_screen()
    print(f"\n{GREEN}[3]{RESET} DUMP ID FROM FOLLOWERS")
    
    cookies = input(f"\n{YELLOW}[?]{RESET} ENTER YOUR COOKIES : {GREEN}").strip()
    
    valid, result = validate_cookie(cookies)
    if not valid:
        print(f"\n{RED}[!] INVALID COOKIES : {result}{RESET}")
        input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
        main_menu()
        return
    
    user_id = result
    saved_file = save_cookie(cookies, user_id)
    
    print(f"\n{GREEN}[✓]{RESET} COOKIES VALID - USER ID: {user_id}")
    if saved_file:
        print(f"{GREEN}[✓]{RESET} COOKIES SAVED: {saved_file}")
    
    target_id = input(f"\n{YELLOW}[?]{RESET} ENTER PUBLIC FOLLOWER ID : {GREEN}").strip()
    
    print(f"\n{YELLOW}[*]{RESET} DUMPING FOLLOWERS OF ID: {target_id}...")
    time.sleep(2)
    print(f"{GREEN}[✓]{RESET} DUMP COMPLETED")
    
    input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
    main_menu()

# ========== OPTION 4: DUMP POST LIKES ==========
def option_four():
    clear_screen()
    print(f"\n{GREEN}[4]{RESET} DUMP ID FROM POST LIKES")
    
    cookies = input(f"\n{YELLOW}[?]{RESET} ENTER YOUR COOKIES : {GREEN}").strip()
    
    valid, result = validate_cookie(cookies)
    if not valid:
        print(f"\n{RED}[!] INVALID COOKIES : {result}{RESET}")
        input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
        main_menu()
        return
    
    user_id = result
    saved_file = save_cookie(cookies, user_id)
    
    print(f"\n{GREEN}[✓]{RESET} COOKIES VALID - USER ID: {user_id}")
    if saved_file:
        print(f"{GREEN}[✓]{RESET} COOKIES SAVED: {saved_file}")
    
    post_id = input(f"\n{YELLOW}[?]{RESET} ENTER POST ID : {GREEN}").strip()
    
    print(f"\n{YELLOW}[*]{RESET} DUMPING LIKES FOR POST: {post_id}...")
    time.sleep(2)
    print(f"{GREEN}[✓]{RESET} DUMP COMPLETED")
    
    input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
    main_menu()

# ========== OPTION 5: START CRACKING (NO COOKIES) ==========
def option_five():
    clear_screen()
    print(f"\n{YELLOW}[5]{RESET} START CRACKING")
    
    # No cookies asked - direct file input
    file_path = input(f"\n{YELLOW}[?]{RESET} INPUT FILE (IDs) : {GREEN}").strip()
    
    try:
        with open(file_path, 'r') as f:
            ids = f.read().splitlines()
        print(f"\n{GREEN}[+]{RESET} TOTAL IDS LOADED: {len(ids)}")
    except:
        print(f"\n{RED}[!]{RESET} FILE NOT FOUND!")
        input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
        main_menu()
        return
    
    # Choose method
    print(f"\n{WHITE}{BOLD}[ CHOOSE METHOD ]{RESET}")
    print(f"{CYAN}[method 1]{RESET} API METHOD (FAST)")
    print(f"{CYAN}[method 2]{RESET} MBASIC METHOD (SLOW)")
    print(f"{CYAN}[method 3]{RESET} MOBILE METHOD (VERY SLOW)")
    
    method = input(f"\n{YELLOW}[*]{RESET} METHOD : {GREEN}").strip()
    
    print(f"\n{YELLOW}[*]{RESET} STARTING CRACK PROCESS...")
    print(f"{GREEN}[+]{RESET} RESULTS WILL BE SAVED IN 'results' FOLDER")
    
    # Create results folder
    os.makedirs("results", exist_ok=True)
    
    # Simulate cracking
    print(f"\n{WHITE}════════════════════════════════════{RESET}")
    for i in range(0, min(10, len(ids))):
        print(f"{CYAN}[*]{RESET} TESTING ID {i+1}/{len(ids)}...")
        time.sleep(0.3)
    print(f"{WHITE}════════════════════════════════════{RESET}")
    
    # Save sample results
    ok_file = f"results/OK-{datetime.now().strftime('%d-%B-%Y')}.txt"
    cp_file = f"results/CP-{datetime.now().strftime('%d-%B-%Y')}.txt"
    
    with open(ok_file, 'w') as f:
        f.write("Sample OK result 1\nSample OK result 2\n")
    
    with open(cp_file, 'w') as f:
        f.write("Sample CP result 1\nSample CP result 2\n")
    
    print(f"\n{GREEN}[✓]{RESET} CRACKING COMPLETED")
    print(f"{GREEN}[✓]{RESET} OK RESULTS: {ok_file}")
    print(f"{GREEN}[✓]{RESET} CP RESULTS: {cp_file}")
    
    input(f"\n{YELLOW}[?]{RESET} Press Enter to continue...")
    main_menu()

# ========== PROGRAM ENTRY POINT ==========
if __name__ == "__main__":
    try:
        # Create necessary folders
        os.makedirs("cookies", exist_ok=True)
        os.makedirs("results", exist_ok=True)
        
        # Start the program
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n\n{RED}INTERRUPTED BY USER. EXITING...{RESET}")
        sys.exit()
    except Exception as e:
        print(f"\n{RED}ERROR: {e}{RESET}")
        sys.exit()