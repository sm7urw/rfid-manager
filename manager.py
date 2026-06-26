import os
import subprocess
import logging
import time
from py532lib.i2c import *
from py532lib.mifare import *

# Setup logging
logging.basicConfig(filename='rfid_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Initiera PN532
pn532 = Mifare()
# Tvinga adressen till 0x24 (Monkey patching)
pn532.address = 0x24

def check_updates():
    print("\n[i] Checking for updates...")
    try:
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        if "Already up to date." in result.stdout:
            print("[+] The script is already up to date.")
        else:
            print("[+] Update completed! Please restart the script.")
    except Exception as e:
        print(f"[-] Update failed: {e}")

def read_log():
    print("\n--- RECENT LOG ENTRIES ---")
    if os.path.exists('rfid_log.txt'):
        with open('rfid_log.txt', 'r') as f:
            print(f.read()[-1000:]) 
    else:
        print("[-] No log file found.")

def print_menu():
    print("\n--- RFID CLI MANAGER ---")
    print("1. Read from Tag X (Copy)")
    print("2. Write to Tag Y (Paste)")
    print("3. Read log file")
    print("4. Check for updates")
    print("5. Exit")
    return input("Choose an option: ")

def main():
    buffer_data = None
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    
    while True:
        choice = print_menu()

      if choice == '1':
            print("\n[!] Please hold Tag X against the reader...")
            try:
                while not pn532.scan_field():
                    time.sleep(0.5)
                
                pn532.mifare_auth_a(4, key)
                data = pn532.mifare_read(4)
                if data:
                    # KONVERTERA TILL LISTA HÄR
                    buffer_data = list(data) 
                    print(f"[+] Success! Data copied: {buffer_data}")
                    logging.info(f"Read successful: {buffer_data}")
            except Exception as e:
                print(f"[-] Read error: {e}") 

        elif choice == '2':
            if buffer_data is None:
                print("[-] Error: Buffer empty. Read a card first!")
                continue
            print("\n[!] Please hold Tag Y against the reader...")
            try:
                # Vänta på att en tagg hittas
                while not pn532.scan_field():
                    time.sleep(0.5)
                    
                pn532.mifare_auth_a(4, key)
                pn532.mifare_write_standard(4, list(buffer_data))
                print("[+] Success! Data written to Tag Y.")
                logging.info("Write successful")
            except Exception as e:
                print(f"[-] Write error: {e}")

        elif choice == '3':
            read_log()
        elif choice == '4':
            check_updates()
        elif choice == '5':
            break

if __name__ == "__main__":
    main()