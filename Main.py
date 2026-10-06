import organizer
import Password_Gen as password_gen
import Disk_Space as disk_space
import ToDo as todo
import Big_Files as big_files
import Duplicates as duplicates
import Renamer as renamer
import Temp_Cleaner as temp_cleaner
from Common import *

apps = [
    ("Downloads Organizer", organizer.run),
    ("Password Generator", password_gen.run),
    ("Disk Space", disk_space.run),
    ("To-Do List", todo.run),
    ("Big File Finder", big_files.run),
    ("Duplicate Finder", duplicates.run),
    ("Bulk Renamer", renamer.run),
    ("Temp Folder Cleaner", temp_cleaner.run),
]

def main():
    while True:
        clear_screen()
        header("Pluto's Helpful App")
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