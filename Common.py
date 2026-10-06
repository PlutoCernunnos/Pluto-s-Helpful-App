import os

Reset = "\033[0m"
Red = "\033[31m"
Green = "\033[32m"
Yellow = "\033[33m"
Blue = "\033[34m"
White = "\033[37m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def header(title):
    print(f"\n{Yellow}===== {title} ====={Reset}")

def pause():
    input(f"\n{White}Press Enter to continue...{Reset}")

def format_size(num_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"

def ask_folder(default):
    path = input(f"{White}Folder path (Enter for {default}): {Reset}").strip().strip('"')
    path = path or default
    if not os.path.isdir(path):
        print(f"{Red}That folder doesn't exist.{Reset}")
        return None
    return path