import os
from Common import *
from organizer import move_to_recycle_bin

def run():
    clear_screen()
    header("Big File Finder")
    start = ask_folder(os.path.expanduser('~'))
    if not start:
        pause()
        return

    print(f"{White}Scanning... this can take a minute.{Reset}")
    files = []
    for root, dirs, names in os.walk(start):
        # Skip hidden folders and AppData (huge, and full of program files)
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'AppData']
        for name in names:
            path = os.path.join(root, name)
            try:
                files.append((os.path.getsize(path), path))
            except OSError:
                pass

    files.sort(reverse=True)
    top = files[:20]
    if not top:
        print(f"{White}No files found.{Reset}")
        pause()
        return

    header("20 Biggest Files")
    for i, (size, path) in enumerate(top, start=1):
        print(f"{White}{i:>2}. {Green}{format_size(size):>10}{White}  {path}{Reset}")

    while True:
        choice = input(f"\n{Yellow}Number to send to Recycle Bin, or q to go back: {Reset}").strip().lower()
        if choice == 'q':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(top):
            size, path = top[int(choice) - 1]
            answer = input(f"{Red}Recycle {os.path.basename(path)} ({format_size(size)})? (y/n): {Reset}")
            if answer.lower() == 'y':
                try:
                    move_to_recycle_bin(path)
                    print(f"{Green}Moved to the Recycle Bin.{Reset}")
                except OSError as error:
                    print(f"{Red}{error}{Reset}")
        else:
            print(f"{Red}Not a valid choice.{Reset}")