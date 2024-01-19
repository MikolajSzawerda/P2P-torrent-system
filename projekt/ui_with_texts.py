import subprocess
import sys

if __name__ == "__main__":

    process = subprocess.run(["python3", "ui.py", "connect"], stdout=sys.stdout, text=True)
    
    while True:
        user_input = input(
            '''Witamy w sieci! 
            \nJeśli chcesz dodać nowy plik wpisz "add"
            \nJeśli chcesz wyszukać plik po nazwie wpisz "search"
            \nJeśli chcesz odłączyć się od systemu wpisz "exit"
            ''')
        
        if(user_input == 'search'):
            process = subprocess.run(["python3", "ui.py", "search"], stdout=sys.stdout, text=True)
            file = input("Wpisz plik, który chcesz pobrać: ")
            md5 = input("Wpisz md5: ")
            process = subprocess.run(["python3", "ui.py", "download", file, md5], stdout=sys.stdout, text=True)
            continue

        if user_input.lower() == 'exit':
            print("Odłączanie od systemu")
            break

        process = subprocess.run(["python3", "ui.py", user_input], stdout=sys.stdout, text=True)

    print("Połączenie zakończone.")
