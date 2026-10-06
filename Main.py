import os
import organizer

Reset = "\033[0m"
Red = "\033[31m"
Green = "\033[32m"
Yellow = "\033[33m"
White = "\033[37m"

# To add an app: make a new .py file with a run() function,
# import it at the top, then add a line to this list.
apps = [
    ("Downloads Organizer", organizer.run),
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        print(f"\n{Yellow}===== Pluto's Helpful App ====={Reset}")
        for i, (name, _) in enumerate(apps, start=1):
            print(f"{White}{i}. {name}{Reset}")
        quit_number = len(apps) + 1
        print(f"{White}{quit_number}. Quit{Reset}")

        choice = input(f"{Yellow}Choose: {Reset}")
        if choice == str(quit_number):
            print(f"{Green}Bye!{Reset}")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(apps):
            apps[int(choice) - 1][1]()
        else:
            input(f"{Red}Pick 1-{quit_number}. Press Enter...{Reset}")

if __name__ == "__main__":
    main()