import time
from py532lib.i2c import *
from py532lib.mifare import *

pn532 = Mifare()
pn532.address = 0x24

def main():
    buffer_data = None
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    
    while True:
        choice = input("\n1. Read (Copy)\n2. Write (Paste)\n5. Exit\nVal: ")
        
        if choice == '1':
            print("[!] Håll Tag X mot läsaren...")
            try:
                while not pn532.scan_field():
                    time.sleep(0.5)
                
                # Använd de inbyggda autentiseringsmetoderna
                pn532.mifare_auth_a(4, key)
                
                # Hämta rådata
                data = pn532.mifare_read(4)
                
                # TVINGA konvertering: Skapa en ny bytearray byte för byte
                buffer_data = bytearray([b for b in data])
                
                print(f"[+] Lyckades! Data i buffert: {list(buffer_data)}")
            except Exception as e:
                print(f"[-] Read error: {e}")

        elif choice == '2':
            if buffer_data is None:
                print("[-] Bufferten är tom!")
                continue
            print("[!] Håll Tag Y mot läsaren...")
            try:
                while not pn532.scan_field():
                    time.sleep(0.5)
                    
                pn532.mifare_auth_a(4, key)
                
                # Skriv direkt med bytearray-objektet
                pn532.mifare_write_standard(4, buffer_data)
                
                print("[+] Lyckades! Skrev data till Tag Y.")
            except Exception as e:
                print(f"[-] Write error: {e}")
        elif choice == '5':
            break

if __name__ == "__main__":
    main()
