import os
import re
import time
from Common import *
from organizer import get_free_name

media_exts = ('.jpg', '.jpeg', '.png', '.heic', '.gif', '.mp4', '.mov')

def photo_date(path, filename):
    # Phone photos usually have the date in the name, like IMG_20261006_183012
    match = re.search(r'(20\d{2})[-_]?(\d{2})[-_]?(\d{2})', filename)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(path)))

def run():
    clear_screen()
    header("Bulk Renamer")
    target = ask_folder(os.path.join(os.path.expanduser('~'), 'Downloads'))
    if not target:
        pause()
        return

    files = sorted(f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f)))
    if not files:
        print(f"{White}No files in that folder.{Reset}")
        pause()
        return

    print(f"{White}1. Add a prefix  2. Replace text  3. Rename photos by date  4. Back{Reset}")
    choice = input(f"{Yellow}Choose: {Reset}")
    plan = []

    if choice == '1':
        prefix = input(f"{White}Prefix to add: {Reset}")
        plan = [(f, prefix + f) for f in files]
    elif choice == '2':
        old = input(f"{White}Text to find: {Reset}")
        new = input(f"{White}Replace with: {Reset}")
        if old:
            plan = [(f, f.replace(old, new)) for f in files if old in f]
    elif choice == '3':
        label = input(f"{White}Label (Enter for 'Photo'): {Reset}").strip() or "Photo"
        photos = [f for f in files if os.path.splitext(f)[1].lower() in media_exts]
        dated = sorted((photo_date(os.path.join(target, f), f), f) for f in photos)
        counters = {}
        for date, f in dated:
            counters[date] = counters.get(date, 0) + 1
            ext = os.path.splitext(f)[1].lower()
            plan.append((f, f"{date} {label} {counters[date]}{ext}"))
    else:
        return

    plan = [(old, new) for old, new in plan if old != new]
    if not plan:
        print(f"{White}Nothing to rename.{Reset}")
        pause()
        return

    header("Preview")
    for old, new in plan[:15]:
        print(f"{White}{old} {Yellow}->{Green} {new}{Reset}")
    if len(plan) > 15:
        print(f"{White}...and {len(plan) - 15} more{Reset}")

    if input(f"\n{Yellow}Rename {len(plan)} files? (y/n): {Reset}").lower() != 'y':
        return

    renamed = 0
    for old, new in plan:
        try:
            os.rename(os.path.join(target, old), get_free_name(target, new))
            renamed += 1
        except OSError as error:
            print(f"{Red}Couldn't rename {old}: {error}{Reset}")
    print(f"{Green}Renamed {renamed} files.{Reset}")
    pause()