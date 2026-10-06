import os
import time
import shutil
import tempfile
from Common import *

def folder_size(path):
    total = 0
    for root, _, names in os.walk(path):
        for name in names:
            try:
                total += os.path.getsize(os.path.join(root, name))
            except OSError:
                pass
    return total

def run():
    clear_screen()
    header("Temp Folder Cleaner")
    temp = tempfile.gettempdir()
    print(f"{White}Temp folder: {Blue}{temp}{Reset}")

    # Only touch things older than a day, since newer ones may still be in use
    cutoff = time.time() - 24 * 3600
    items = []
    total = 0
    for name in os.listdir(temp):
        path = os.path.join(temp, name)
        try:
            if os.path.getmtime(path) > cutoff:
                continue
            size = folder_size(path) if os.path.isdir(path) else os.path.getsize(path)
        except OSError:
            continue
        items.append(path)
        total += size

    if not items:
        print(f"{Green}Nothing old enough to clean.{Reset}")
        pause()
        return

    print(f"{Yellow}Found {len(items)} items older than 1 day ({format_size(total)}).{Reset}")
    if input(f"{Red}Delete them permanently? (y/n): {Reset}").lower() != 'y':
        return

    deleted = skipped = 0
    for path in items:
        try:
            if os.path.isdir(path) and not os.path.islink(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            deleted += 1
        except OSError:
            skipped += 1  # in use by a running program; that's normal

    print(f"{Green}Deleted {deleted} items.{Reset}")
    if skipped:
        print(f"{White}Skipped {skipped} that are in use.{Reset}")
    pause()