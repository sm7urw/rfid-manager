from py532lib.i2c import *
from py532lib.mifare import *

# Skapa objektet
pn532 = Mifare()

# Skriv ut alla tillgängliga metoder
print("--- METODER SOM FINNS I DITT BIBLIOTEK ---")
for m in dir(pn532):
    if not m.startswith("__"):
        print(m)