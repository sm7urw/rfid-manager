import os
import subprocess
import logging
import time
from py532lib.i2c import *
from py532lib.mifare import *

# Setup logging
logging.basicConfig(filename='rfid_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

pn532 = Mifare()
pn532.address = 0x24

def main():
    buffer_data = None
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    
    while True:
        choice = input("\n1. Read (Copy)\n2. Write (Paste)\n5. Exit\nVal: ")
        
        if choice == '1':
            print("\n[!] Håll Tag X mot läsaren...")
            try:
                while not pn532.scan_field():
                    time.sleep(0.5)
                
                pn532.mifare_auth_a(4, key)
                
                # RÅ LÄSNING: Vi skickar kommandot manuellt istället för att anropa mifare_read()
                # 0x30 är Mifare Read-kommandot, följt av blocknummer 4
                data = pn532.call_command(bytearray([0x30, 4]), 20)
                
                # Spara datan (PN532 skickar ofta tillbaka ett svar med extra bytes)
                # Vi tar de 16 sista bytesen som faktiskt är datat
                buffer_data = data[-16:]
                
                print(f"[+] Lyckades! Kopierade data: {list(buffer_data)}")
            except Exception as e:
                print(f"[-] Read error (Manuell): {e}")

        elif choice == '2':
            if buffer_data is None:
                print("[-] Bufferten är tom!")
                continue
            print("\n[!] Håll Tag Y mot läsaren...")
            try:
                while not pn532.scan_field():
                    time.sleep(0.5)
                
                pn532.mifare_auth_a(4, key)
                
                # RÅ SKRIVNING: Vi skickar Write-kommandot (0xA0) och block (4)
                # Sedan lägger vi till datat (buffer_data)
                cmd = bytearray([0xA0, 4]) + buffer_data
                pn532.call_command(cmd, 20)
                
                print("[+] Lyckades! Skrev data till Tag Y.")
            except Exception as e:
                print(f"[-] Write error: {e}")
        elif choice == '5':
            break

if __name__ == "__main__":
    main()
