import argparse
from cryptography.fernet import Fernet
from colorama import init, Back, Style

init()

## Generera och spara en krypteringsnyckel ##
def generera_nyckel():
    key = Fernet.generate_key() #Genererar en nyckel
    with open("nyckelfil.key", "wb") as key_file: #Gör en ny fil för att spara nyckeln i
        key_file.write(key)
    print("Den genererade nyckeln har sparats i 'nyckelfil.key'")

## Ladda nyckel ##
def ladda_nyckel():
    with open("nyckelfil.key", "rb") as key_file: #Laddar en nyckel så den kan anändas för kryptering/dekryptering
        return key_file.read()

## Kryptering ##
def kryptera_fil(filnamn, nyckel):
    cipher_suite = Fernet(nyckel) #skapar en cipher_suite som innehåller nyckeln så att vi kan kryptera
    with open(filnamn, "rb") as file: #läser in vad filen innehåller i binärt format
        fil_data = file.read()
    
    krypterad_data = cipher_suite.encrypt(fil_data) #krypterar datan i filen och lagrar den i en variabel
    with open(f"{filnamn}.enc", "wb") as file: #skapar en ny krypterad fil
        file.write(krypterad_data)
    print(f"Filen '{filnamn}' har krypterats och sparats som '{filnamn}.enc'")

## Dekryptering ##
def dekryptera_fil(filnamn, nyckel):
    cipher_suite = Fernet(nyckel) #skapar en cipher_suite som innehåller nyckeln så att vi kan dekryptera
    with open(filnamn, "rb") as file: #läser in vad som står i filen 
        krypterad_data = file.read()
    
    dekrypterad_data = cipher_suite.decrypt(krypterad_data) #dekrypterar datan i den krypterade filen
    dekrypterat_filnamn = "dekrypterad_" + filnamn.replace(".enc", "") #byter filtyp till .jpg istället för .enc
    with open(dekrypterat_filnamn, "wb") as file: #skapar en ny fil
        file.write(dekrypterad_data)
    print(f"Filen '{filnamn}' har dekrypterats och sparats som '{dekrypterat_filnamn}'")

## Huvudfunktion ##

def mainscript():
    print(Back.GREEN + "KRYPTERINGSVERKTYG" + Style.RESET_ALL)
    parser = argparse.ArgumentParser(description="Kryptera och dekryptera filer")
    parser.add_argument("operation", choices=["generera", "kryptera", "dekryptera"], help="Operation att utföra")
    parser.add_argument("filnamn", nargs = "?", help="Fil att kryptera eller dekryptera")
    parser.add_argument("-v", "--verbose", action="store_true", help="Visa mer information")
    args = parser.parse_args()

    if args.operation == "generera":
        generera_nyckel() #anropar funktionen om användaren skriver generera i konsolen
    elif args.operation == "kryptera":
        if not args.filnamn: #om användaren inte skriver namnet på filen som ska krypteras
            print("Ange en fil att kryptera")
        else:
            nyckel = ladda_nyckel() #laddar upp nyckeln så att kryptering kan påbörjas
            kryptera_fil(args.filnamn, nyckel)
    elif args.operation == "dekryptera":
        if not args.filnamn: #om användaren inte skriver namnet på filen som ska dekrypteras
            print("Ange en fil att dekryptera")
        else:
            nyckel = ladda_nyckel() #laddar upp nyckeln så att dekryptering kan påbörjas
            dekryptera_fil(args.filnamn, nyckel)
if __name__ == "__main__":
    mainscript()
