import os
import time
import json

settings_file = 'Organizer_settings.json'

default_settings = {
    "delete_empty_folders": True,
    "delete_after_days": 30,
    "delete_ignore": ["Audio", "Videos", "Images", "Documents"]
}

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            return json.load(f)
    return default_settings

def save_settings(settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)

settings = load_settings()

Reset = "\033[0m"
Red = "\033[31m"
Green = "\033[32m"
Yellow = "\033[33m"
White = "\033[37m"
blue = "\033[34m"

folder = os.path.join(os.path.expanduser('~'), 'Downloads')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[2J\033[H', end='', flush=True)

categories = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
    'installers': ['.exe', '.msi', '.dmg'],
    'Others': []
}

def get_free_name(destination, filename):
    new_path = os.path.join(destination, filename)
    if not os.path.exists(new_path):
        return new_path
    name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(new_path):
        new_path = os.path.join(destination, f"{name} ({counter}){ext}")
        counter += 1
    return new_path

def Organize_Files():
    report = {}
    total_moved = 0

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            age_days = (time.time() - os.path.getmtime(file_path)) / (24 * 3600)
            moved = False
            for category, extensions in categories.items():
                if file_ext in extensions:
                    category_folder = os.path.join(folder, category)
                    if age_days > settings["delete_after_days"]:
                        destination = os.path.join(category_folder, "Old_Files")
                    else:
                        destination = os.path.join(category_folder, "New_Files")
                    os.makedirs(destination, exist_ok=True)
                    new_file_path = get_free_name(destination, filename)
                    os.rename(file_path, new_file_path)
                    report[category] = report.get(category, 0) + 1
                    total_moved += 1
                    print(f"{Green}Moved {filename} to {blue}{destination}{Reset}")
                    moved = True
                    break
            if not moved:
                others_folder = os.path.join(folder, 'Others')
                os.makedirs(others_folder, exist_ok=True)
                new_file_path = get_free_name(others_folder, filename)
                os.rename(file_path, new_file_path)
                print(f"{Green}Moved {filename} to {blue}{new_file_path}{Reset}")
                report['Others'] = report.get('Others', 0) + 1
                total_moved += 1

    print(f"\n{Yellow}===== Summary of Moved Files ====={Reset}")
    if total_moved == 0:
        print(f"{White}Nothing to move. All files are already organized.{Reset}")
    else:
        for category, count in report.items():
            print(f"{White}{category}: files moved {Green}{count}{Reset}")
        print(f"{Yellow}Total files moved: {Green}{total_moved}{Reset}")

def Cleanup_old_files():
    print(f"\n{Yellow}===== Old file cleanup ====={Reset}")

    # Phase 1: scan everything first
    folders_with_old = {}
    for category in categories:
        if category in settings["delete_ignore"]:
            continue

        old_files_folder = os.path.join(folder, category, "Old_Files")
        if not os.path.exists(old_files_folder):
            continue

        old_files = []
        total_size = 0
        for filename in os.listdir(old_files_folder):
            file_path = os.path.join(old_files_folder, filename)
            age_days = (time.time() - os.path.getmtime(file_path)) / (24 * 3600)
            if age_days > settings["delete_after_days"]:
                old_files.append(file_path)
                total_size += os.path.getsize(file_path)

        if old_files:
            folders_with_old[category] = (old_files, total_size)

    if settings["delete_empty_folders"] is True:
        for category in categories:
            old_files_folder = os.path.join(folder, category, "Old_Files")
            if os.path.exists(old_files_folder) and not os.listdir(old_files_folder):
                os.rmdir(old_files_folder)
                print(f"{Green}Deleted empty folder: {old_files_folder}{Reset}")

    if not folders_with_old:
        print(f"{White}No old files to clean up.{Reset}")
        return

    # Phase 2: menu loop
    while folders_with_old:
        print(f"\n{Yellow}Folders with old files:{Reset}")
        options = list(folders_with_old.keys())
        for i, category in enumerate(options, start=1):
            old_files, total_size = folders_with_old[category]
            total_mb = total_size / (1024 * 1024)
            print(f"{White}{i}. {category} — {len(old_files)} files, {total_mb:.2f} MB{Reset}")

        choice = input(f"{Yellow}Pick a number to clean, 'a' for all, or 'q' to quit: {Reset}").lower()

        if choice == 'q':
            break

        if choice == 'a':
            picked = options
        elif choice.isdigit() and 1 <= int(choice) <= len(options):
            picked = [options[int(choice) - 1]]
        else:
            print(f"{Red}Not a valid choice.{Reset}")
            continue

        for category in picked:
            old_files, total_size = folders_with_old[category]
            answer = input(f"{Red}{category}: delete all {len(old_files)} old files? (y/n): {Reset}")
            if answer.lower() == 'y':
                for file_path in old_files:
                    os.remove(file_path)
                    print(f"{Red}Deleted {os.path.basename(file_path)}{Reset}")
            else:
                answer = input(f"{Red}Delete individual files? (y/n): {Reset}")
                if answer.lower() == 'y':
                    for file_path in old_files:
                        filename = os.path.basename(file_path)
                        size = os.path.getsize(file_path) / (1024 * 1024)
                        answer = input(f"{Red}Delete {filename} ({size:.2f} MB)? (y/n): {Reset}")
                        if answer.lower() == 'y':
                            os.remove(file_path)
                            print(f"{Red}Deleted {filename}{Reset}")
            del folders_with_old[category]
   

def Settings_Menu():
    while True:
        print(f"\n{Yellow}===== Settings ====={Reset}")
        print(f"{White}1. Days before 'old' (currently {settings['delete_after_days']}){Reset}")
        print(f"{White}2. Ignored categories (currently: {', '.join(settings['delete_ignore'])}){Reset}")
        print(f"{White}3. Back to main menu{Reset}")

        choice = input(f"{Yellow}Choose: {Reset}")

        if choice == '1':
            new_days = input(f"{White}New number of days: {Reset}")
            if new_days.isdigit():
                settings['delete_after_days'] = int(new_days)
                save_settings(settings)
                print(f"{Green}Saved!{Reset}")
            else:
                print(f"{Red}That's not a number.{Reset}")

        elif choice == '2':
            name = input(f"{White}Type a category to add/remove from ignore list: {Reset}")
            if name in settings['delete_ignore']:
                settings['delete_ignore'].remove(name)
                save_settings(settings)
                print(f"{Green}{name} removed — it will now get cleanup prompts.{Reset}")
            elif name in categories:
                settings['delete_ignore'].append(name)
                save_settings(settings)
                print(f"{Green}{name} added to ignore list.{Reset}")
            else:
                print(f"{Red}No category called '{name}'. Options: {', '.join(categories)}{Reset}")

        elif choice == '3':
            break

# ===== Main menu =====
while True:
    clear_screen()
    print(f"\n{Yellow}===== Downloads Organizer ====={Reset}")
    print(f"{White}1. Organize now{Reset}")
    print(f"{White}2. Clean up old files{Reset}")
    print(f"{White}3. Settings{Reset}")
    print(f"{White}4. Open Downloads folder{Reset}")
    print(f"{White}5. Quit{Reset}")

    choice = input(f"{Yellow}Choose: {Reset}")

    if choice == '1':
        Organize_Files()
    elif choice == '2':
        Cleanup_old_files()
    elif choice == '3':
        Settings_Menu()
    elif choice == '4':
        os.startfile(folder)
    elif choice == '5':
        print(f"{Green}Bye!{Reset}")
        break
    else:
        print(f"{Red}Pick 1-5.{Reset}")

    if choice != '5':
        input(f"\n{White}Press Enter to return to the menu...{Reset}")
