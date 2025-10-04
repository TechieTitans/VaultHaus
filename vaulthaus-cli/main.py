import os
import sys
import pandas as pd
import random
import time
from tabulate import tabulate

 
FILENAME = "vaulthaus_data.xlsx"
LETTER = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
NUMBER = "0123456789"
SYMBOL = r"/*-.},.;'[]\=-?><|+_)!@$%#^&*("


def load_vault():
     
    if not os.path.exists(FILENAME):
        return []
    try:
        df = pd.read_excel(FILENAME)
        df.fillna('', inplace=True)
        return df.to_dict('records')
    except Exception as e:
        print(f"🚨 Error loading data: {e}")
        sys.exit(1)

def save_vault(vault_items):
     
    try:
        
        df = pd.DataFrame(vault_items, columns=["Service", "Username", "Password"])
        df.to_excel(FILENAME, index=False)
    except Exception as e:
        print(f"🚨 Error saving data: {e}")

 

def _create_new_password():
    """Internal helper to generate a single strong password."""
    tips = [["1", "Letters (a-z, A-Z)", "8 to 12"],
            ["2", "Numbers (0-9)", "2 to 4"],
            ["3", "Symbols (!@#$%)", "2 to 4"]]
    header = ["No.", "Characters", "Ideal Proportion of Characters"]
    print("\nTip For Creating Strong Passwords:")
    print(tabulate(tips, headers=header, tablefmt="grid"))

    try:
        letter_count = int(input("How many letters :  "))
        number_count = int(input("How many numbers :  "))
        symbol_count = int(input("How many symbols :  "))

        
    except ValueError:
        print("\n❌ Invalid input. Using default counts.")
        letter_count, number_count, symbol_count = 10, 3, 3

    password_list = []
    password_list.extend(random.choice(LETTER) for _ in range(letter_count))
    password_list.extend(random.choice(NUMBER) for _ in range(number_count))
    password_list.extend(random.choice(SYMBOL) for _ in range(symbol_count))
    
    random.shuffle(password_list)
    return "".join(password_list)


def view_vault(vault_items):
    print("\n--- 🔐 Your VaultHaus Items ---")
    if not vault_items:
        print("Your vault is empty! Generate an item to get started. ✨")
    else:
        headers = ["#", "Service", "Username", "Password"]
        display_data = [[i, d.get('Service', 'N/A'), d.get('Username', 'N/A'), d.get('Password', 'N/A')] 
                        for i, d in enumerate(vault_items, 1)]
        print(tabulate(display_data, headers=headers, tablefmt="grid"))
     


def generate_new_vault_item(vault_items):
    print("\n--- Generate a New Vault Item ---")
    service = input("Which Service or Website is this for? (e.g, Github , Google , Hugging face):  ").strip()
    username = input(f"What is your actual Username for '{service}':  ").strip()

    if not service or not username:
        print("\n⚠️ Service and Username cannot be empty. Aborting.")
        return

    generated_password = _create_new_password()

    print(f"\n   Service: {service}")
    print(f"   Username: {username}")
     
    print("\nGenerating", end="", flush=True)
    for _ in range(5):
      print(".", end="", flush=True)
      time.sleep(0.5)

    sys.stdout.write("\r" + " " * 30 + "\r")   
    sys.stdout.flush()

    print(f"   Password: {generated_password}")

    new_entry = {"Service": service, "Username": username, "Password": generated_password}
    vault_items.append(new_entry)
    save_vault(vault_items)
    print("\n✅ Add new vault Sucessfully.")

def update_vault_item(vault_items):
    view_vault(vault_items)

    if not vault_items:
        return

    try:
        choice_str = input("Enter the number of the item to update: > ")
        item_index = int(choice_str) - 1

        if 0 <= item_index < len(vault_items):
            old_entry = vault_items[item_index]
            print(f"\nUpdating item for '{old_entry.get('Service')}'...")
            
            new_service = input(f"New service ({old_entry.get('Service')}): > ").strip() or old_entry.get('Service')
            new_username = input(f"New username ({old_entry.get('Username')}): > ").strip() or old_entry.get('Username')

            prompt = (
                "New password: Press Enter to keep\n"
                "(m) manual type\n"
                "(g) generate from generator\n> "
            )
            pass_choice = input(prompt).lower().strip()
            
            if pass_choice == 'm':
                new_password = input("Enter new manual password: > ").strip()
                if not new_password:
                    print("   Manual password cannot be empty. Keeping original.")
                    new_password = old_entry.get('Password')
            elif pass_choice == 'g':
                new_password = _create_new_password()
                print(f"   Your new generated password is: {new_password}")
            else:
                new_password = old_entry.get('Password')
                if pass_choice:
                    print("   Invalid choice. Keeping original password.")

            vault_items[item_index] = {"Service": new_service, "Username": new_username, "Password": new_password}
            save_vault(vault_items)
            print(f"\n✅ Successfully updated vault item for: '{new_service}'.")
        else:
            print("\n❌ Invalid number. Please choose a number from the list.")
    except ValueError:
        print("\n❌ Invalid input. Please enter a number.")

def delete_vault_item(vault_items):
    view_vault(vault_items)

    if not vault_items:
        return

    try:
        choice_str = input("Enter the number of the item to DELETE: > ")
        item_index = int(choice_str) - 1

        if 0 <= item_index < len(vault_items):
            item_to_delete = vault_items[item_index]
            
            confirm = input(f"🚨 Are you sure you want to delete the item for '{item_to_delete.get('Service')}'? (y/n): ").lower().strip()
            
            if confirm == 'y':
                deleted = vault_items.pop(item_index)
                save_vault(vault_items)
                print(f"\n✅ Successfully deleted vault item for: '{deleted.get('Service')}'.")
            else:
                print("\nDeletion cancelled.")
        else:
            print("\n❌ Invalid number. Please choose a number from the list.")
    except ValueError:
        print("\n❌ Invalid input. Please enter a number.")


def show_menu():
    """Displays the main menu."""
    print("\n==========================================================================")
    print("                           Welcome to VaultHaus \n")
    print("                   Your vault. Your rules. Your password. ")
    print("============================================================================")
    print("(1) View Vault")
    print("(2) Generate a new vault item")  
    print("(3) Update an existing vault item") 
    print("(4) Delete an existing vault item")
    print("(5) Quit") 
    print("----------------------------------------------------------------------------")

def main():
    vault_items = load_vault()
    
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == '1':
            view_vault(vault_items)
        elif choice == '2':
            generate_new_vault_item(vault_items)
        elif choice == '3':
            update_vault_item(vault_items)
        elif choice == '4':
            delete_vault_item(vault_items)  
        elif choice == '5':
            print("\nExiting VaultHaus. Goodbye! 👋")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 5.")
        
        input("\n(Press Enter to continue...)")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()