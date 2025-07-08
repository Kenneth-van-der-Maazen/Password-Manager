import os
from cryptography.fernet import Fernet

os.system("mode con cols=50 lines=20")
clear = lambda: os.system('clear')

class PasswordManager:
    
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.username_dict = {}
        
    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
            
    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
            
    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        
        with open(path, 'w') as f:
            f.write(f"KEY:{self.key.decode()}\n")
        
        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)
            
    def load_password_file(self, path):
        self.password_file = path
        
        with open(path, 'r') as f:
            next(f)
            for line in f:
                try:
                    site, login, encrypted = line.strip().split(":")
                    decrypted_password = Fernet(self.key).decrypt(encrypted.encode()).decode()
                    self.password_dict[site] = decrypted_password
                    self.username_dict[site] = login
                except ValueError:
                    print(f"[WAARSCHUWING] Ongeldige regel overgeslagen: {line.strip()}")
                
    def add_password(self, site, login, password):
        self.password_dict[site] = password
        self.username_dict[site] = login
        
        if self.password_file is not None:
            with open(self.password_file, 'r+') as f:
                lines = f.readlines()
                
                if not lines or not lines[0].startswith("KEY:"):
                    lines.insert(0, f"KEY:{self.key.decode()}\n")
                    
                encrypted = Fernet(self.key).encrypt(password.encode())
                lines.append(f"{site}:{login}:{encrypted.decode()}\n")
                
                f.seek(0)
                f.writelines(lines)
            
            
    def get_password(self, site):
        return self.password_dict[site]
    


def main():
    
    clear()
    
    # password = {}
    pm = PasswordManager()
    
    # === Vraag naar key bij opstarten ===
    while True:
        input_key = input("Enter Key: ")
        if not input_key.endswith(".key"):
            input_key += ".key"
            
        if os.path.exists(input_key):
            try: 
                pm.load_key(input_key)
                clear()
                print(f"[OK] Keys loaded!\n")
                break
            except Exception as e:
                print(f"[ERROR] Unable to load key: {e}")
                
        else:
            keuze = input(f"[!] Keyfab '{input_key}' not found... \nCreate as new key? (y/n): ").strip()
            if keuze.lower() in ("y", "yes"):
                try:
                    pm.create_key(input_key)
                    clear()
                    print(f"[OK] New {input_key} created!\n")
                    input("Press Enter to continue...")
                    clear()
                    break
                except Exception as e:
                    print(f"[ERROR] Unable to create key: {e}\n")
                    
            else:
                clear()
                print("Please try again...\n")

    #=== Menu ===
    menu = """Select an option:
    (1) Create new password list
    (2) Load existing passwords from file
    (3) Add a new password 
    (4) Get passwords from list
    
    (q) Quit    
    """
    
    done = False
    
    while not done:        
        print(f"{menu}")
        choice = input("Enter an option: ")
        
        if choice == "1":
            # clear()
            path = input("Filename: ")
            if not path.endswith(".pass"):
                path += ".pass"
            
            with open(path, 'w') as f:
                pass
            
            pm.create_password_file(path)
            
            clear()
            print(f"[OK] New password list '{path}' created.\n")
            input("Press Enter to continue...")
            clear()
            
        elif choice == "2":
            # clear()
            path = input("Path to file passwordlist: ")
            if os.path.exists(path):
                pm.load_password_file(path)
                print(f"Passwords from list '{path}' loaded.\n")
                input("Press Enter to continue...")
                clear()
            else:
                print("[!] File not found.\n")
                input("Press Enter to continue...")
                clear()
            
        elif choice == "3":
            site = input("Site: ")
            login = input("Login: ")
            pwd = input("Password: ")
            pm.add_password(site, login, pwd)
            print(f"[OK] Password: '{site}' added.\n")
            input("Press Enter to continue...")
            clear()
            
        elif choice == "4":
            site = input("Site name: ")
            try:
                clear()
                login = pm.username_dict[site]
                pwd = pm.get_password(site)
                print(f"[>>] Login credentials: [{site}]")
                print(f"     Username: {login}")
                print(f"     Password: {pwd}\n")
                input("Press Enter to return...")
                clear()
            except KeyError:
                print("[!] No login credentials found for this site.\n")
                input("Press Enter to continue...")
                clear()
            
        elif choice == "q":
            done = True
            print("Bye!")
            
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
    

# pm = PasswordManager()
# pm.create_key("mykey.key")